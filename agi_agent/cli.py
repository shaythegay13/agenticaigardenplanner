import argparse
import time
import readline  # For better input handling
from typing import Optional, Sequence
from .core.agent import AGIAgent
from .gardening.models import (
    UserInput,
    LocationInput,
    GardeningMethod,
    SpaceSize,
    Sunlight,
    Experience,
    UserGoals,
    CropInterest,
    Preference,
    SoilType,
)
from .gardening.climate import geocode_location, fetch_simple_forecast
from .gardening.planner import generate_plan
from .gardening.vision import analyze_garden_image

def run_interview():
    print("Welcome to the Gardening Plan Generator")
    print("Answer a few questions to get a customized plan. Press Ctrl+C to exit.\n")

    try:
        # Location input
        use_address = input("Do you want to enter an address? (y/n) ").strip().lower() == 'y'
        if use_address:
            address = input("Enter address: ").strip()
            location = LocationInput(address=address)
        else:
            lat = float(input("Enter latitude (e.g., 40.7128): ").strip())
            lon = float(input("Enter longitude (e.g., -74.0060): ").strip())
            location = LocationInput(latitude=lat, longitude=lon)

        # Method
        print("\nChoose gardening method:")
        methods = list(GardeningMethod)
        for i, m in enumerate(methods, 1):
            print(f"  {i}. {m.value}")
        method = methods[int(input("Your choice #: ").strip()) - 1]

        # Size
        print("\nChoose space size:")
        sizes = list(SpaceSize)
        for i, s in enumerate(sizes, 1):
            print(f"  {i}. {s.value}")
        size = sizes[int(input("Your choice #: ").strip()) - 1]

        # Sunlight
        print("\nChoose sunlight exposure:")
        lights = list(Sunlight)
        for i, s in enumerate(lights, 1):
            print(f"  {i}. {s.value}")
        sunlight = lights[int(input("Your choice #: ").strip()) - 1]

        # Experience
        print("\nChoose experience level:")
        exps = list(Experience)
        for i, e in enumerate(exps, 1):
            print(f"  {i}. {e.value}")
        experience = exps[int(input("Your choice #: ").strip()) - 1]

        # Soil type
        print("\nChoose soil type (for water management analysis):")
        soil_types = list(SoilType)
        for i, st in enumerate(soil_types, 1):
            print(f"  {i}. {st.value}")
        soil_choice = input("Your choice # (or blank for unknown): ").strip()
        soil_type = soil_types[int(soil_choice) - 1] if soil_choice else SoilType.UNKNOWN

        # Goals
        print("\nSelect crop interests (comma-separated numbers):")
        crops_all = list(CropInterest)
        for i, c in enumerate(crops_all, 1):
            print(f"  {i}. {c.value}")
        crop_indices = [int(x.strip()) for x in input("Your choices: ").split(',') if x.strip()]
        crops = [crops_all[i-1] for i in crop_indices]

        print("\nSelect preferences (optional, comma-separated numbers or blank to skip):")
        prefs_all = list(Preference)
        for i, p in enumerate(prefs_all, 1):
            print(f"  {i}. {p.value}")
        raw = input("Your choices: ").strip()
        preferences = []
        if raw:
            pref_indices = [int(x.strip()) for x in raw.split(',') if x.strip()]
            preferences = [prefs_all[i-1] for i in pref_indices]
        notes = input("Any additional notes? (optional): ").strip() or None

        # Image path
        image_path = input("Provide an image path of your space (optional, blank to skip): ").strip() or None

        # Resolve location and climate
        lat, lon = geocode_location(location)
        climate = fetch_simple_forecast(lat, lon)

        user_input = UserInput(
            location=LocationInput(latitude=lat, longitude=lon, address=getattr(location, 'address', None)),
            method=method,
            size=size,
            sunlight=sunlight,
            experience=experience,
            soil_type=soil_type,
            goals=UserGoals(crops=crops, preferences=preferences, notes=notes),
            image_path=image_path,
        )

        print("\nGenerating your customized plan...\n")
        start = time.time()
        vision = None
        if image_path:
            vision = analyze_garden_image(image_path)
        plan = generate_plan(user_input, climate, vision_insights=vision)
        duration = time.time() - start

        print(plan)
        print(f"\n[Generated in {duration:.2f}s]")

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\nError: {e}\n")

def run_optional_voice(args: argparse.Namespace) -> int:
    """Text answers always run. Speech runs only when a Deepgram key is set."""
    from .gardening.voice import (
        SPEECH_DISABLED_MESSAGE,
        VoiceDependencyError,
        VoiceDisabledError,
        ask_question,
        speech_enabled,
        transcribe_audio,
        voice_status,
    )

    if args.status or (args.voice and not args.ask and not args.transcribe):
        status = voice_status()
        print(f"speech: {status['voice']}")
        print(f"answers: {status['answer_source']}")
        if status["message"]:
            print(status["message"])
        if args.voice and not args.ask and not args.transcribe and not args.status:
            print("Ask a question with: python -m agi_agent.cli --ask \"What should I plant in spring?\"")
        if not args.ask and not args.transcribe:
            return 0

    if args.transcribe:
        if not speech_enabled():
            print(SPEECH_DISABLED_MESSAGE)
            return 2
        try:
            with open(args.transcribe, "rb") as audio_file:
                audio = audio_file.read()
        except OSError as exc:
            print(f"Could not read audio file: {exc}")
            return 2
        try:
            print(transcribe_audio(audio))
        except VoiceDisabledError as exc:
            print(exc)
            return 2
        except (VoiceDependencyError, ValueError) as exc:
            print(exc)
            return 2
        return 0

    try:
        result = ask_question(text=args.ask, speak=bool(args.voice and speech_enabled()))
    except ValueError as exc:
        print(exc)
        return 2
    print(result.answer_text)
    if args.voice and result.audio:
        path = "garden_advice.mp3"
        with open(path, "wb") as audio_file:
            audio_file.write(result.audio)
        print(f"Audio saved to {path}")
    elif args.voice and not result.speech_enabled:
        print(SPEECH_DISABLED_MESSAGE)
    return 0


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser(description="Ask Jane garden planner")
    parser.add_argument("--ask", metavar="QUESTION", help="Answer one garden question from the local catalogs")
    parser.add_argument("--voice", action="store_true", help="Speak the answer when DEEPGRAM_API_KEY is set")
    parser.add_argument("--transcribe", metavar="AUDIO", help="Transcribe an audio file when speech is enabled")
    parser.add_argument("--status", action="store_true", help="Print whether speech is enabled")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.status or args.ask is not None or args.transcribe or args.voice:
        code = run_optional_voice(args)
        if argv is None:
            raise SystemExit(code)
        return code
    run_interview()


if __name__ == "__main__":
    main()
