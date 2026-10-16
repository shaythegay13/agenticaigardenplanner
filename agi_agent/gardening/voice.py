"""
Optional voice for Ask Jane.

Speech-to-text and text-to-speech use Deepgram when DEEPGRAM_API_KEY is set.
Question wording can use OpenAI when OPENAI_API_KEY is set. With neither key,
questions are answered from the catalogs in this repository and speech stays off.

Neither provider is imported until a call actually needs it.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence

try:
    from dotenv import load_dotenv

    load_dotenv()
    # Fill names that are still empty. Does not override a key already set.
    load_dotenv(".env.local")
except ImportError:
    pass

from .care_guides import get_care_guide
from .climate import fetch_simple_forecast, geocode_location
from .companion_planting import COMPANION_DATABASE
from .crop_timing import CROP_TIMING_DATABASE, CropTiming, get_crop_timing
from .disease_identifier import identify_disease_from_image
from .knowledge import PLANTS
from .models import (
    CropInterest,
    Experience,
    GardeningMethod,
    LocationInput,
    Preference,
    SoilType,
    SpaceSize,
    Sunlight,
    UserGoals,
    UserInput,
)
from .planner import generate_plan

SPEECH_DISABLED_MESSAGE = (
    "Voice is disabled because DEEPGRAM_API_KEY is not set. "
    "The garden planner still answers in text from the local catalogs."
)

MAX_AUDIO_BYTES = 8_000_000
MAX_SPEAK_CHARS = 4500

_SEASON_PRIORITY = {
    "Spring": ["lettuce", "spinach", "radish", "peas", "carrot", "broccoli", "kale", "beet"],
    "Summer": ["tomato", "pepper", "cucumber", "basil", "beans", "zucchini", "eggplant"],
    "Fall": ["kale", "spinach", "lettuce", "broccoli", "carrot", "beet", "peas"],
    "Winter": ["kale", "spinach", "garlic", "onion"],
}

_DISEASE_WORDS = (
    "spot",
    "spots",
    "mildew",
    "wilt",
    "blight",
    "mold",
    "mould",
    "rot",
    "yellow",
    "curl",
    "rust",
    "lesion",
    "disease",
    "sick",
    "fungus",
    "pest",
)

_CROP_INTERESTS = (
    (("tomato",), CropInterest.TOMATOES),
    (("pepper",), CropInterest.PEPPERS),
    (("lettuce", "spinach", "kale", "greens"), CropInterest.LEAFY_GREENS),
    (("basil", "mint", "cilantro", "parsley", "herb"), CropInterest.HERBS),
    (("carrot", "radish", "beet", "root"), CropInterest.ROOT_VEGETABLES),
    (("bean", "pea"), CropInterest.BEANS_PEAS),
    (("cucumber", "squash", "zucchini"), CropInterest.SQUASH_CUCUMBERS),
    (("onion", "garlic"), CropInterest.ONIONS_GARLIC),
    (("strawberry", "blueberry", "raspberry", "berry"), CropInterest.BERRIES),
    (("microgreen",), CropInterest.MICROGREENS),
    (("apple", "pear", "citrus", "fruit tree"), CropInterest.FRUIT_TREES),
)


class VoiceDisabledError(RuntimeError):
    """Speech was requested and DEEPGRAM_API_KEY is empty."""


class VoiceDependencyError(RuntimeError):
    """A speech or model key is set, but the optional package is missing or unusable."""


@dataclass
class VoiceAnswer:
    transcript: Optional[str]
    answer_text: str
    audio: Optional[bytes]
    speech_enabled: bool
    answer_source: str


@dataclass
class GardenPlanVoiceResult:
    transcript: str
    extracted_params: Dict[str, Any]
    plan: str
    summary: str
    audio: Optional[bytes]
    speech_enabled: bool
    parameter_source: str
    _enums: Dict[str, Any] = field(repr=False, default_factory=dict)


def _key(name: str) -> str:
    return os.environ.get(name, "").strip()


def speech_enabled() -> bool:
    """True when a Deepgram key is present. Does not call Deepgram."""
    return bool(_key("DEEPGRAM_API_KEY"))


def openai_enabled() -> bool:
    """True when an OpenAI key is present. Does not call OpenAI."""
    return bool(_key("OPENAI_API_KEY"))


def voice_status() -> Dict[str, Any]:
    enabled = speech_enabled()
    return {
        "speech_enabled": enabled,
        "voice": "enabled" if enabled else "disabled",
        "openai_enabled": openai_enabled(),
        "answer_source": "openai" if openai_enabled() else "local",
        "message": None if enabled else SPEECH_DISABLED_MESSAGE,
    }


def _require_speech() -> None:
    if not speech_enabled():
        raise VoiceDisabledError(SPEECH_DISABLED_MESSAGE)


def _deepgram_client():
    _require_speech()
    try:
        from deepgram import DeepgramClient
    except ImportError as exc:
        raise VoiceDependencyError(
            "DEEPGRAM_API_KEY is set, but the deepgram package is not installed. "
            "Install the optional voice extra: pip install 'deepgram-sdk>=3' 'openai>=1'."
        ) from exc
    key = _key("DEEPGRAM_API_KEY")
    try:
        return DeepgramClient(api_key=key)
    except TypeError:
        return DeepgramClient(key)


def _transcript_from_response(response: Any) -> str:
    results = getattr(response, "results", None)
    if results is None and isinstance(response, dict):
        results = response.get("results")
    if isinstance(results, dict):
        channels = results.get("channels") or []
    else:
        channels = getattr(results, "channels", None) or []
    if not channels:
        raise VoiceDependencyError("Deepgram returned a transcript response with no channels.")
    channel = channels[0]
    if isinstance(channel, dict):
        alternatives = channel.get("alternatives") or []
    else:
        alternatives = getattr(channel, "alternatives", None) or []
    if not alternatives:
        raise VoiceDependencyError("Deepgram returned a transcript response with no alternatives.")
    alternative = alternatives[0]
    if isinstance(alternative, dict):
        transcript = alternative.get("transcript")
    else:
        transcript = getattr(alternative, "transcript", None)
    if transcript is None:
        raise VoiceDependencyError("Deepgram returned an empty transcript field.")
    return str(transcript).strip()


def _collect_audio(response: Any) -> bytes:
    if isinstance(response, (bytes, bytearray)):
        return bytes(response)
    stream = getattr(response, "stream", None)
    if isinstance(stream, (bytes, bytearray)):
        return bytes(stream)
    if hasattr(stream, "read"):
        data = stream.read()
        return data if isinstance(data, (bytes, bytearray)) else b""
    stream_memory = getattr(response, "stream_memory", None)
    if hasattr(stream_memory, "getvalue"):
        return stream_memory.getvalue()
    if isinstance(stream_memory, (bytes, bytearray)):
        return bytes(stream_memory)
    audio = bytearray()
    try:
        iterator = iter(response)
    except TypeError as exc:
        raise VoiceDependencyError("Deepgram returned a speech response that could not be read.") from exc
    for chunk in iterator:
        if isinstance(chunk, (bytes, bytearray)):
            audio.extend(chunk)
        elif isinstance(chunk, str):
            audio.extend(chunk.encode())
        else:
            data = getattr(chunk, "data", None)
            if isinstance(data, (bytes, bytearray)):
                audio.extend(data)
            elif isinstance(data, str):
                audio.extend(data.encode())
    return bytes(audio)


def transcribe_audio(audio: bytes) -> str:
    """Transcribe speech. Raises VoiceDisabledError when no speech key is set."""
    _require_speech()
    if not audio:
        raise ValueError("Audio is empty.")
    if len(audio) > MAX_AUDIO_BYTES:
        raise ValueError("Audio is larger than 8 MB.")
    client = _deepgram_client()
    listen = client.listen
    media = getattr(getattr(listen, "v1", None), "media", None)
    if media is not None and hasattr(media, "transcribe_file"):
        response = media.transcribe_file(
            request=audio,
            model="nova-3",
            smart_format=True,
        )
        return _transcript_from_response(response)
    prerecorded = getattr(listen, "prerecorded", None)
    if prerecorded is not None and hasattr(prerecorded, "v"):
        try:
            from deepgram import PrerecordedOptions

            options = PrerecordedOptions(model="nova-2", smart_format=True)
        except ImportError:
            options = {"model": "nova-2", "smart_format": True}
        response = prerecorded.v("1").transcribe_file({"buffer": audio}, options)
        return _transcript_from_response(response)
    raise VoiceDependencyError(
        "The installed deepgram package does not expose a transcription method. "
        "Install deepgram-sdk and retry."
    )


def synthesize_speech(text: str) -> bytes:
    """Synthesize speech. Raises VoiceDisabledError when no speech key is set."""
    _require_speech()
    spoken = (text or "").strip()
    if not spoken:
        raise ValueError("Nothing to speak.")
    if len(spoken) > MAX_SPEAK_CHARS:
        spoken = spoken[: MAX_SPEAK_CHARS - 1].rstrip() + "…"
    client = _deepgram_client()
    speak = client.speak
    audio_api = getattr(getattr(speak, "v1", None), "audio", None)
    if audio_api is not None and hasattr(audio_api, "generate"):
        response = audio_api.generate(text=spoken, model="aura-asteria-en")
        data = _collect_audio(response)
        if not data:
            raise VoiceDependencyError("Deepgram returned no audio bytes.")
        return data
    if hasattr(speak, "v"):
        try:
            from deepgram import SpeakOptions

            options = SpeakOptions(model="aura-asteria-en")
        except ImportError:
            options = {"model": "aura-asteria-en"}
        response = speak.v("1").stream({"text": spoken}, options)
        data = _collect_audio(response)
        if not data:
            raise VoiceDependencyError("Deepgram returned no audio bytes.")
        return data
    raise VoiceDependencyError(
        "The installed deepgram package does not expose a speech synthesis method. "
        "Install deepgram-sdk and retry."
    )


def _phrase_in(text: str, phrase: str) -> bool:
    pattern = r"\b" + re.escape(phrase.lower()) + r"(?:es|s)?\b"
    return re.search(pattern, text) is not None


def mentioned_crops(text: str, limit: int = 3) -> List[str]:
    """Timing-catalog keys named in text, longer names first."""
    lowered = text.lower()
    phrases = []
    for key, timing in CROP_TIMING_DATABASE.items():
        phrases.append((timing.name.lower(), key))
        phrases.append((key.replace("_", " "), key))
    phrases.sort(key=lambda item: len(item[0]), reverse=True)
    found: List[str] = []
    for phrase, key in phrases:
        if len(phrase) < 4:
            continue
        if key in found:
            continue
        if _phrase_in(lowered, phrase):
            found.append(key)
        if len(found) >= limit:
            break
    return found


def _season_name(text: str) -> Optional[str]:
    lowered = text.lower()
    if re.search(r"\bspring\b", lowered):
        return "Spring"
    if re.search(r"\bsummer\b", lowered):
        return "Summer"
    if re.search(r"\b(fall|autumn)\b", lowered):
        return "Fall"
    if re.search(r"\bwinter\b", lowered):
        return "Winter"
    return None


def _crops_for_season(season: str, limit: int = 6) -> List[CropTiming]:
    found: List[CropTiming] = []
    seen = set()
    for key in _SEASON_PRIORITY.get(season, []):
        timing = CROP_TIMING_DATABASE.get(key)
        if timing and season in timing.planting_season and key not in seen:
            found.append(timing)
            seen.add(key)
    if len(found) < limit:
        for key, timing in CROP_TIMING_DATABASE.items():
            if key in seen:
                continue
            if season in timing.planting_season:
                found.append(timing)
                seen.add(key)
            if len(found) >= limit:
                break
    return found[:limit]


def _companion_record(crop_key: str):
    timing = get_crop_timing(crop_key)
    name = timing.name if timing else crop_key.replace("_", " ")
    candidates = [name.lower(), crop_key.replace("_", " "), crop_key]
    if not name.lower().endswith("s"):
        candidates.append(name.lower() + "s")
    for candidate in candidates:
        if candidate in COMPANION_DATABASE:
            return candidate, COMPANION_DATABASE[candidate]
    for key, info in COMPANION_DATABASE.items():
        if _candidate_match(key, candidates):
            return key, info
    return None, None


def _candidate_match(key: str, candidates: Sequence[str]) -> bool:
    for candidate in candidates:
        if key in candidate or candidate in key:
            return True
    return False


def _join_names(names: Iterable[str], limit: int = 5) -> str:
    shown = [name.replace("_", " ") for name in list(names)[:limit]]
    if not shown:
        return ""
    if len(shown) == 1:
        return shown[0]
    return ", ".join(shown[:-1]) + f", and {shown[-1]}"


def _location_clause(location: Optional[str]) -> str:
    if location and location.strip():
        return f" in {location.strip()}"
    return ""


def _answer_season(season: str, location: Optional[str]) -> str:
    crops = _crops_for_season(season)
    place = _location_clause(location)
    lines = [
        f"For {season.lower()} planting{place}, these crops are in the timing catalog."
    ]
    for timing in crops:
        note = (timing.notes or "").strip()
        if note and not note.endswith("."):
            note += "."
        sentence = (
            f"{timing.name}: plant in {', '.join(timing.planting_months)}. "
            f"About {timing.days_to_harvest} days to harvest."
        )
        if note:
            sentence = f"{sentence} {note}"
        lines.append(sentence)
    lines.append(
        "Check the local last-frost date before moving warm-season transplants outside. "
        "A written bed plan is available from the garden plan endpoint."
    )
    return " ".join(lines)


def _answer_timing(crop_key: str, location: Optional[str]) -> str:
    timing = get_crop_timing(crop_key)
    if not timing:
        return _answer_starter(location)
    place = _location_clause(location)
    indoor = ""
    if timing.indoor_start_weeks:
        indoor = (
            f" Start seeds indoors about {timing.indoor_start_weeks} weeks before the last frost."
        )
    note = (timing.notes or "").strip()
    if note and not note.endswith("."):
        note += "."
    return (
        f"{timing.name}{place}: plant in {', '.join(timing.planting_months)} "
        f"({', '.join(timing.planting_season)}). "
        f"About {timing.days_to_harvest} days to harvest, "
        f"typically in {', '.join(timing.harvest_months)}.{indoor} "
        f"{note}"
    ).strip()


def _answer_companion(crop_key: str) -> str:
    matched, info = _companion_record(crop_key)
    timing = get_crop_timing(crop_key)
    name = timing.name if timing else crop_key.replace("_", " ")
    if not info:
        return (
            f"The companion catalog does not have a specific list for {name}. "
            "A full plan still includes companion notes for the crops it suggests."
        )
    good = _join_names(info.good_companions)
    bad = _join_names(info.bad_companions)
    benefit = ""
    if info.benefits:
        first = next(iter(info.benefits))
        label_name = first.replace("_", " ")
        detail = str(info.benefits[first]).strip()
        if detail and not detail.endswith("."):
            detail += "."
        benefit = f" {label_name[:1].upper()}{label_name[1:]}: {detail}"
    label = matched.replace("_", " ") if matched else name
    return (
        f"Companions listed for {label} include {good}. "
        f"Plants to keep separate include {bad}.{benefit}"
    )


def _answer_care(crop_key: str) -> str:
    timing = get_crop_timing(crop_key)
    name = timing.name if timing else crop_key.replace("_", " ")
    guide = get_care_guide(crop_key) or get_care_guide(name)
    if not guide:
        return (
            f"There is no care note filed under {name}. "
            "The written garden plan includes a care schedule for suggested crops."
        )
    parts = [f"Care notes for {name}."]
    if guide.get("watering"):
        parts.append(f"Watering: {guide['watering']}")
    if guide.get("fertilization"):
        parts.append(f"Feeding: {guide['fertilization']}")
    if guide.get("pruning"):
        parts.append(f"Pruning: {guide['pruning']}")
    tasks = guide.get("common_tasks") or []
    if tasks:
        parts.append("Also: " + " ".join(tasks[:2]))
    return " ".join(parts)


def _catalog_crop_name(crop_key: str) -> str:
    """Prefer a name the family catalog actually stores."""
    from .crop_families import CROP_FAMILIES

    timing = get_crop_timing(crop_key)
    name = timing.name if timing else crop_key.replace("_", " ")
    candidates = [name, crop_key.replace("_", " "), f"{name}s", f"{name}es"]
    for candidate in candidates:
        if candidate.lower().replace(" ", "_") in CROP_FAMILIES:
            return candidate
    return name


def _answer_disease(question: str, crops: Sequence[str]) -> str:
    crop_name = _catalog_crop_name(crops[0]) if crops else None
    result = identify_disease_from_image(crop_name=crop_name, symptoms=[question])
    if not result.matches:
        named = f" on {crop_name}" if crop_name else ""
        return (
            f"No disease note matched those symptoms{named}. "
            "Name the crop and what the leaves or fruit look like, or send the same words to "
            "the disease endpoint. This service matches keywords. It does not inspect a photo."
        )
    top = result.matches[0]
    prevention = " ".join(top.prevention[:2]) if top.prevention else ""
    treatment = " ".join(top.treatment[:2]) if top.treatment else ""
    crop_bit = f" for {crop_name}" if crop_name else ""
    return (
        f"The closest local note{crop_bit} is {top.disease_name} ({top.confidence} confidence). "
        f"{top.description} "
        f"{prevention} {treatment}"
    ).strip()


def _answer_starter(location: Optional[str]) -> str:
    place = _location_clause(location)
    beginners = [
        plant for plant in PLANTS
        if Experience.BEGINNER in plant.experience
    ][:5]
    if not beginners:
        beginners = PLANTS[:5]
    names = _join_names(plant.name for plant in beginners)
    notes = " ".join(f"{plant.name}: {plant.notes}" for plant in beginners[:3])
    return (
        f"Ask Jane can plan a bed{place} from a location, a method, and a space size. "
        f"Beginner-friendly plants in the short catalog include {names}. {notes} "
        "Ask about a season, a crop, companions, watering, or symptoms for a more specific note."
    )


def answer_from_catalogs(
    question: str,
    context: Optional[dict] = None,
    location: Optional[str] = None,
) -> str:
    """Answer from the checked-in catalogs. Does not call a paid API."""
    text = (question or "").strip()
    if not text:
        raise ValueError("Question is empty.")
    lowered = text.lower()
    crops = mentioned_crops(text)
    season = _season_name(text)
    disease = any(re.search(rf"\b{word}\b", lowered) for word in _DISEASE_WORDS)
    companion = any(
        token in lowered
        for token in ("companion", "plant with", "next to", "alongside", "interplant")
    )
    care = any(token in lowered for token in ("water", "fertil", "prune", "how do i care", "care for"))

    if disease:
        answer = _answer_disease(text, crops)
    elif companion and crops:
        answer = _answer_companion(crops[0])
    elif care and crops:
        answer = _answer_care(crops[0])
    elif crops and any(token in lowered for token in ("when", "plant", "sow", "transplant")):
        answer = _answer_timing(crops[0], location)
    elif season and any(token in lowered for token in ("plant", "sow", "grow", "vegetable", "crop")):
        answer = _answer_season(season, location)
    elif season:
        answer = _answer_season(season, location)
    elif crops:
        answer = _answer_timing(crops[0], location)
    else:
        answer = _answer_starter(location)

    if context:
        extra = ", ".join(f"{key}: {value}" for key, value in list(context.items())[:4])
        if extra:
            answer = f"{answer} Context you sent: {extra}."
    return answer


def _answer_with_openai(question: str, context: Optional[dict], location: Optional[str]) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise VoiceDependencyError(
            "OPENAI_API_KEY is set, but the openai package is not installed. "
            "Install it with: pip install 'openai>=1'."
        ) from exc
    client = OpenAI(api_key=_key("OPENAI_API_KEY"))
    system_prompt = (
        "You are an expert garden planning assistant. Provide helpful, "
        "practical advice about gardening, planting, crop care, and garden planning. "
        "Keep responses concise but informative (2-3 paragraphs max for voice output). "
        "Focus on actionable advice."
    )
    user_prompt = question
    if location:
        user_prompt = f"Location: {location}\n\nQuestion: {user_prompt}"
    if context:
        user_prompt = f"Context: {context}\n\n{user_prompt}"
    completion = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = completion.choices[0].message.content
    if not content or not str(content).strip():
        raise VoiceDependencyError("OpenAI returned an empty answer.")
    return str(content).strip()


def answer_garden_question(
    question: str,
    context: Optional[dict] = None,
    location: Optional[str] = None,
) -> tuple:
    """Return (answer_text, source). Source is 'openai' or 'local'."""
    if openai_enabled():
        try:
            return _answer_with_openai(question, context, location), "openai"
        except Exception:
            return answer_from_catalogs(question, context, location), "local"
    return answer_from_catalogs(question, context, location), "local"


def ask_question(
    text: Optional[str] = None,
    audio: Optional[bytes] = None,
    context: Optional[dict] = None,
    location: Optional[str] = None,
    speak: bool = True,
) -> VoiceAnswer:
    """
    Answer a garden question.

    Audio is transcribed only when speech is enabled. Text answers do not need a key.
    Spoken audio is included only when speech is enabled and speak is true.
    """
    transcript = None
    if audio:
        transcript = transcribe_audio(audio)
        question = transcript
    elif text and text.strip():
        question = text.strip()
    else:
        raise ValueError("Provide a text question or audio.")
    if not question:
        raise ValueError("The transcript was empty.")

    answer_text, source = answer_garden_question(question, context=context, location=location)
    audio_out = None
    enabled = speech_enabled()
    if speak and enabled:
        audio_out = synthesize_speech(answer_text)
    return VoiceAnswer(
        transcript=transcript,
        answer_text=answer_text,
        audio=audio_out,
        speech_enabled=enabled,
        answer_source=source,
    )


def _crop_interests_from_text(text: str) -> List[CropInterest]:
    lowered = text.lower()
    found: List[CropInterest] = []
    for words, interest in _CROP_INTERESTS:
        if any(_phrase_in(lowered, word) or word in lowered for word in words):
            if interest not in found:
                found.append(interest)
    return found or [CropInterest.SUGGEST]


def _preferences_from_text(text: str) -> List[Preference]:
    lowered = text.lower()
    found: List[Preference] = []
    checks = (
        (("drought",), Preference.DROUGHT_RESISTANT),
        (("low maintenance", "easy"), Preference.LOW_MAINTENANCE),
        (("native",), Preference.NATIVE),
        (("pest",), Preference.PEST_RESISTANT),
        (("fast",), Preference.FAST_GROWING),
        (("minimal water", "little water"), Preference.MIN_WATER),
    )
    for words, preference in checks:
        if any(word in lowered for word in words):
            found.append(preference)
    return found


def _seasons_from_text(text: str) -> Optional[List[str]]:
    found = []
    for label, pattern in (
        ("Spring", r"\bspring\b"),
        ("Summer", r"\bsummer\b"),
        ("Fall", r"\b(fall|autumn)\b"),
        ("Winter", r"\bwinter\b"),
    ):
        if re.search(pattern, text.lower()):
            found.append(label)
    return found or None


def extract_garden_parameters(text: str) -> Dict[str, Any]:
    """
    Map a spoken or written request onto planner enums.

    Uses OpenAI when that key is set, and keyword matching otherwise.
    Unstated fields use the same defaults as a short raised-bed plan.
    """
    if openai_enabled():
        try:
            parsed = _extract_with_openai(text)
            return _normalize_extracted(parsed, text)
        except Exception:
            pass
    return _extract_with_keywords(text)


def _extract_with_keywords(text: str) -> Dict[str, Any]:
    lowered = text.lower()
    method = GardeningMethod.RAISED_BEDS
    if "container" in lowered or re.search(r"\bpots?\b", lowered):
        method = GardeningMethod.CONTAINERS
    elif "hydro" in lowered:
        method = GardeningMethod.HYDROPONIC
    elif "indoor" in lowered or "windowsill" in lowered:
        method = GardeningMethod.INDOOR
    elif "vertical" in lowered or "trellis" in lowered:
        method = GardeningMethod.VERTICAL
    elif "rooftop" in lowered or re.search(r"\broof\b", lowered):
        method = GardeningMethod.ROOFTOP
    elif "in-ground" in lowered or "in ground" in lowered or "inground" in lowered:
        method = GardeningMethod.IN_GROUND

    size = SpaceSize.MEDIUM
    if "very large" in lowered or "community" in lowered:
        size = SpaceSize.VERY_LARGE
    elif "large" in lowered or "backyard" in lowered:
        size = SpaceSize.LARGE
    elif "small" in lowered or "windowsill" in lowered:
        size = SpaceSize.SMALL

    sunlight = Sunlight.FULL_SUN
    if "grow light" in lowered or "artificial" in lowered:
        sunlight = Sunlight.ARTIFICIAL_LIGHTS
    elif "partial shade" in lowered:
        sunlight = Sunlight.PARTIAL_SHADE
    elif "partial" in lowered:
        sunlight = Sunlight.PARTIAL_SUN
    elif re.search(r"\bshade\b", lowered):
        sunlight = Sunlight.SHADE

    experience = Experience.BEGINNER
    if "advanced" in lowered or "experienced" in lowered:
        experience = Experience.ADVANCED
    elif "intermediate" in lowered:
        experience = Experience.INTERMEDIATE
    elif "novice" in lowered:
        experience = Experience.NOVICE

    return _parameter_dict(
        method,
        size,
        sunlight,
        experience,
        _crop_interests_from_text(text),
        _preferences_from_text(text),
        _seasons_from_text(text),
        "keywords",
    )


def _parameter_dict(method, size, sunlight, experience, crops, preferences, seasons, source) -> Dict[str, Any]:
    return {
        "method": method,
        "size": size,
        "sunlight": sunlight,
        "experience": experience,
        "crop_interests": crops,
        "preferences": preferences,
        "seasons": seasons,
        "parameter_source": source,
    }


def _match_enum(enum_cls, raw: Optional[str], default):
    if not raw:
        return default
    text = str(raw).strip().lower()
    for item in enum_cls:
        if item.value.lower() == text or item.name.lower() == text or text in item.value.lower():
            return item
    aliases = {
        GardeningMethod: {
            "container": GardeningMethod.CONTAINERS,
            "containers": GardeningMethod.CONTAINERS,
            "pot": GardeningMethod.CONTAINERS,
            "raised bed": GardeningMethod.RAISED_BEDS,
            "raised beds": GardeningMethod.RAISED_BEDS,
            "in-ground": GardeningMethod.IN_GROUND,
            "inground": GardeningMethod.IN_GROUND,
            "vertical": GardeningMethod.VERTICAL,
            "indoor": GardeningMethod.INDOOR,
            "rooftop": GardeningMethod.ROOFTOP,
            "hydroponic": GardeningMethod.HYDROPONIC,
        },
        SpaceSize: {
            "small": SpaceSize.SMALL,
            "medium": SpaceSize.MEDIUM,
            "large": SpaceSize.LARGE,
            "very large": SpaceSize.VERY_LARGE,
        },
        Sunlight: {
            "full sun": Sunlight.FULL_SUN,
            "partial sun": Sunlight.PARTIAL_SUN,
            "partial shade": Sunlight.PARTIAL_SHADE,
            "shade": Sunlight.SHADE,
            "artificial": Sunlight.ARTIFICIAL_LIGHTS,
        },
        Experience: {
            "beginner": Experience.BEGINNER,
            "novice": Experience.NOVICE,
            "intermediate": Experience.INTERMEDIATE,
            "advanced": Experience.ADVANCED,
        },
    }
    table = aliases.get(enum_cls, {})
    for key, item in table.items():
        if key in text:
            return item
    return default


def _extract_with_openai(text: str) -> Dict[str, Any]:
    import json

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise VoiceDependencyError(
            "OPENAI_API_KEY is set, but the openai package is not installed."
        ) from exc
    client = OpenAI(api_key=_key("OPENAI_API_KEY"))
    prompt = (
        "Extract garden planning parameters from this request: "
        f"{text}\n\n"
        "Return a JSON object with these fields (use null if not mentioned):\n"
        "- method: Container, Raised Beds, In-ground, Vertical, Indoor, Rooftop, Hydroponic\n"
        "- size: Small, Medium, Large, Very Large\n"
        "- sunlight: Full Sun, Partial Sun, Partial Shade, Shade\n"
        "- experience: Beginner, Novice, Intermediate, Advanced\n"
        "- crops: list of crop interests\n"
        "- preferences: list like low maintenance, drought resistant\n"
        "- address: location if mentioned\n"
        "Only return the JSON, no other text."
    )
    completion = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": prompt}],
    )
    content = completion.choices[0].message.content or ""
    start = content.find("{")
    end = content.rfind("}")
    if start < 0 or end < start:
        raise ValueError("OpenAI did not return JSON.")
    return json.loads(content[start : end + 1])


def _normalize_extracted(parsed: Dict[str, Any], text: str) -> Dict[str, Any]:
    crops = _crop_interests_from_text(" ".join(parsed.get("crops") or []) + " " + text)
    preference_text = " ".join(parsed.get("preferences") or []) + " " + text
    params = _parameter_dict(
        _match_enum(GardeningMethod, parsed.get("method"), GardeningMethod.RAISED_BEDS),
        _match_enum(SpaceSize, parsed.get("size"), SpaceSize.MEDIUM),
        _match_enum(Sunlight, parsed.get("sunlight"), Sunlight.FULL_SUN),
        _match_enum(Experience, parsed.get("experience"), Experience.BEGINNER),
        crops,
        _preferences_from_text(preference_text),
        _seasons_from_text(text),
        "openai",
    )
    address = parsed.get("address")
    if isinstance(address, str) and address.strip():
        params["address"] = address.strip()
    return params


def _public_params(params: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "method": params["method"].value,
        "size": params["size"].value,
        "sunlight": params["sunlight"].value,
        "experience": params["experience"].value,
        "crops": [crop.value for crop in params["crop_interests"]],
        "preferences": [item.value for item in params["preferences"]],
        "seasons": params.get("seasons"),
    }


def garden_plan_from_description(
    text: str,
    address: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    speak: bool = True,
) -> GardenPlanVoiceResult:
    """
    Build a written plan from a short description.

    Geocoding and the forecast run only when coordinates are not already provided.
    Speech audio is attached only when DEEPGRAM_API_KEY is set.
    """
    description = (text or "").strip()
    if not description:
        raise ValueError("Describe the garden you want, or send audio of that description.")
    params = extract_garden_parameters(description)
    stated_address = (address or "").strip() or params.get("address") or ""
    if latitude is not None and longitude is not None:
        location = LocationInput(
            address=stated_address or None,
            latitude=latitude,
            longitude=longitude,
        )
    else:
        if not stated_address:
            raise ValueError(
                "Location is required for a garden plan. Pass an address, or latitude and longitude."
            )
        location = LocationInput(address=stated_address)
        lat, lon = geocode_location(location)
        location.latitude = lat
        location.longitude = lon

    climate = fetch_simple_forecast(location.latitude, location.longitude)
    user_input = UserInput(
        location=location,
        method=params["method"],
        size=params["size"],
        sunlight=params["sunlight"],
        experience=params["experience"],
        soil_type=SoilType.MEDIUM,
        goals=UserGoals(
            crops=params["crop_interests"],
            preferences=params["preferences"],
            notes=description[:500],
        ),
        seasons=params.get("seasons"),
    )
    plan_text = generate_plan(user_input, climate)
    place = climate.city or stated_address or "your location"
    summary = (
        f"I made a garden plan for a {params['size'].value} {params['method'].value} garden near {place}. "
        "The full written plan includes crop ideas, a bed sketch, watering notes, companions, and care. "
        "The complete text is in the plan field."
    )
    audio = synthesize_speech(summary) if speak and speech_enabled() else None
    return GardenPlanVoiceResult(
        transcript=description,
        extracted_params=_public_params(params),
        plan=plan_text,
        summary=summary,
        audio=audio,
        speech_enabled=speech_enabled(),
        parameter_source=params["parameter_source"],
    )
