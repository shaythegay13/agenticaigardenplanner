#!/usr/bin/env python3
"""Voice stays optional: no speech key, no provider import, text answers still work."""

import base64
import os
import sys
import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

os.environ.pop("DEEPGRAM_API_KEY", None)
os.environ.pop("OPENAI_API_KEY", None)

from agi_agent.cli import main as cli_main
from agi_agent.gardening.models import (
    ClimateData,
    CropInterest,
    Experience,
    GardeningMethod,
    SpaceSize,
    Sunlight,
)
from agi_agent.gardening.voice import (
    SPEECH_DISABLED_MESSAGE,
    VoiceDisabledError,
    answer_from_catalogs,
    ask_question,
    extract_garden_parameters,
    garden_plan_from_description,
    speech_enabled,
    synthesize_speech,
    transcribe_audio,
    voice_status,
)
from api import app
from fastapi.testclient import TestClient


def _climate():
    return ClimateData(
        latitude=40.7128,
        longitude=-74.006,
        timezone="America/New_York",
        daily_highs_c=[18, 19, 17, 16, 20, 21, 15],
        daily_lows_c=[8, 9, 7, 6, 10, 11, 5],
        daily_precip_mm=[0, 1, 0, 2, 0, 0, 4],
        summary="Mild week",
        city="New York",
        state="New York",
        us_region="Northeast",
        usda_zone="7",
    )


class VoiceTestCase(unittest.TestCase):
    def setUp(self):
        self._saved = {
            name: os.environ.get(name)
            for name in ("DEEPGRAM_API_KEY", "OPENAI_API_KEY")
        }
        os.environ.pop("DEEPGRAM_API_KEY", None)
        os.environ.pop("OPENAI_API_KEY", None)

    def tearDown(self):
        for name, value in self._saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


class TestSpeechDisabled(VoiceTestCase):
    def test_status_is_disabled_without_importing_providers(self):
        status = voice_status()
        self.assertFalse(speech_enabled())
        self.assertFalse(status["speech_enabled"])
        self.assertEqual(status["voice"], "disabled")
        self.assertEqual(status["answer_source"], "local")
        self.assertIn("DEEPGRAM_API_KEY", status["message"])
        self.assertNotIn("deepgram", sys.modules)
        self.assertNotIn("openai", sys.modules)

    def test_transcribe_and_speak_raise_a_clean_error(self):
        for call in (lambda: transcribe_audio(b"abc"), lambda: synthesize_speech("hello")):
            with self.assertRaises(VoiceDisabledError) as caught:
                call()
            self.assertEqual(str(caught.exception), SPEECH_DISABLED_MESSAGE)
        self.assertNotIn("deepgram", sys.modules)

    def test_blank_key_is_the_same_as_unset(self):
        os.environ["DEEPGRAM_API_KEY"] = "   "
        self.assertFalse(speech_enabled())
        with self.assertRaises(VoiceDisabledError):
            transcribe_audio(b"abc")


class TestCatalogAnswers(VoiceTestCase):
    def test_spring_planting_uses_the_timing_catalog(self):
        answer = answer_from_catalogs(
            "What vegetables should I plant in spring?",
            location="New York, NY",
        )
        self.assertIn("Lettuce", answer)
        self.assertIn("New York, NY", answer)
        self.assertIn("spring", answer.lower())

    def test_carrot_timing_companions_and_watering(self):
        timing = answer_from_catalogs("When should I plant carrots?")
        self.assertIn("March", timing)
        companions = answer_from_catalogs("What should I plant with tomatoes?")
        self.assertIn("basil", companions.lower())
        care = answer_from_catalogs("How do I water tomatoes?")
        self.assertIn("Watering:", care)

    def test_symptom_question_uses_the_disease_notes(self):
        answer = answer_from_catalogs("My tomato leaves have brown spots with target rings")
        self.assertTrue(
            "blight" in answer.lower() or "spot" in answer.lower(),
            answer,
        )

    def test_ask_without_a_speech_key_returns_text_and_no_audio(self):
        result = ask_question(
            text="What vegetables should I plant in spring?",
            context={"experience": "beginner"},
            speak=True,
        )
        self.assertIsNone(result.transcript)
        self.assertIsNone(result.audio)
        self.assertFalse(result.speech_enabled)
        self.assertEqual(result.answer_source, "local")
        self.assertIn("beginner", result.answer_text)
        self.assertIn("Lettuce", result.answer_text)

    def test_openai_failure_falls_back_to_the_catalog(self):
        os.environ["OPENAI_API_KEY"] = "test-key-not-a-secret"
        with patch(
            "agi_agent.gardening.voice._answer_with_openai",
            side_effect=RuntimeError("quota"),
        ):
            text, source = __import__(
                "agi_agent.gardening.voice", fromlist=["answer_garden_question"]
            ).answer_garden_question("What vegetables should I plant in spring?")
        self.assertEqual(source, "local")
        self.assertIn("Lettuce", text)

    def test_openai_answer_is_used_when_the_call_succeeds(self):
        os.environ["OPENAI_API_KEY"] = "test-key-not-a-secret"
        with patch(
            "agi_agent.gardening.voice._answer_with_openai",
            return_value="Plant peas early.",
        ):
            from agi_agent.gardening.voice import answer_garden_question

            text, source = answer_garden_question("What vegetables should I plant in spring?")
        self.assertEqual(source, "openai")
        self.assertEqual(text, "Plant peas early.")
        self.assertNotIn("openai", sys.modules)


class TestSpeechClient(VoiceTestCase):
    def _transcript_response(self, text):
        alternative = MagicMock()
        alternative.transcript = text
        channel = MagicMock()
        channel.alternatives = [alternative]
        response = MagicMock()
        response.results.channels = [channel]
        return response

    def test_v5_transcribe_and_speak_use_the_client_and_not_the_network(self):
        os.environ["DEEPGRAM_API_KEY"] = "test-key-not-a-secret"
        client = MagicMock()
        client.listen.v1.media.transcribe_file.return_value = self._transcript_response(
            "what should I plant in spring"
        )
        client.speak.v1.audio.generate.return_value = [b"ID3", b"audio"]
        with patch("agi_agent.gardening.voice._deepgram_client", return_value=client):
            self.assertEqual(
                transcribe_audio(b"not-real-audio"),
                "what should I plant in spring",
            )
            self.assertEqual(synthesize_speech("Hello garden"), b"ID3audio")
        client.listen.v1.media.transcribe_file.assert_called_once()
        self.assertNotIn("deepgram", sys.modules)

    def test_older_sdk_shape_is_used_when_v1_is_missing(self):
        os.environ["DEEPGRAM_API_KEY"] = "test-key-not-a-secret"
        transcript = self._transcript_response("peas")

        class Recorder:
            def v(self, version):
                return self

            def transcribe_file(self, payload, options):
                return transcript

        class Speaker:
            def v(self, version):
                return self

            def stream(self, payload, options):
                class Clip:
                    stream = b"mp3-bytes"
                return Clip()

        class Listen:
            prerecorded = Recorder()

        class Client:
            listen = Listen()
            speak = Speaker()

        with patch("agi_agent.gardening.voice._deepgram_client", return_value=Client()):
            self.assertEqual(transcribe_audio(b"audio"), "peas")
            self.assertEqual(synthesize_speech("Hello"), b"mp3-bytes")


class TestGardenPlanWords(VoiceTestCase):
    def test_keywords_map_onto_current_enums(self):
        params = extract_garden_parameters(
            "I want a small container garden of tomatoes. I am a beginner and I want low maintenance plants in partial shade."
        )
        self.assertEqual(params["method"], GardeningMethod.CONTAINERS)
        self.assertEqual(params["size"], SpaceSize.SMALL)
        self.assertEqual(params["sunlight"], Sunlight.PARTIAL_SHADE)
        self.assertEqual(params["experience"], Experience.BEGINNER)
        self.assertIn(CropInterest.TOMATOES, params["crop_interests"])
        self.assertEqual(params["parameter_source"], "keywords")

    def test_plan_uses_generate_plan_without_a_speech_key(self):
        with patch(
            "agi_agent.gardening.voice.fetch_simple_forecast",
            return_value=_climate(),
        ) as forecast:
            result = garden_plan_from_description(
                "I want a small container garden of tomatoes",
                address="New York, NY",
                latitude=40.7128,
                longitude=-74.006,
                speak=True,
            )
        forecast.assert_called_once()
        self.assertIsNone(result.audio)
        self.assertFalse(result.speech_enabled)
        self.assertIn("container", result.summary.lower())
        self.assertIn("Tomatoes", result.plan)
        self.assertEqual(result.extracted_params["method"], GardeningMethod.CONTAINERS.value)

    def test_missing_location_is_a_value_error(self):
        with self.assertRaises(ValueError) as caught:
            garden_plan_from_description("a small raised bed")
        self.assertIn("Location is required", str(caught.exception))


class TestApiVoiceDisabled(VoiceTestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_crops_and_voice_status(self):
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "healthy")
        self.assertEqual(health.json()["voice"], "disabled")
        self.assertEqual(health.json()["answers"], "local")
        status = self.client.get("/api/voice/status")
        self.assertEqual(status.status_code, 200)
        self.assertFalse(status.json()["speech_enabled"])
        crops = self.client.get("/api/crops")
        self.assertEqual(crops.status_code, 200)
        self.assertGreater(crops.json()["total_crops"], 0)
        root = self.client.get("/")
        self.assertEqual(root.json()["voice"], "disabled")
        self.assertIn("voice_question", root.json()["endpoints"])

    def test_text_question_has_no_audio(self):
        response = self.client.post(
            "/api/voice/ask",
            json={
                "text_question": "What vegetables should I plant in spring?",
                "location": "New York, NY",
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("Lettuce", body["answer_text"])
        self.assertIsNone(body["audio_base64"])
        self.assertFalse(body["speech_enabled"])
        self.assertEqual(body["answer_source"], "local")

    def test_audio_routes_are_disabled(self):
        encoded = base64.b64encode(b"not-audio").decode("ascii")
        asked = self.client.post("/api/voice/ask", json={"audio_base64": encoded})
        self.assertEqual(asked.status_code, 503)
        self.assertIn("DEEPGRAM_API_KEY", asked.json()["detail"])
        spoken = self.client.post("/api/voice/speak", data={"text": "Hello garden"})
        self.assertEqual(spoken.status_code, 503)
        self.assertIn("disabled", spoken.json()["detail"].lower())
        uploaded = self.client.post(
            "/api/voice/upload",
            files={"audio_file": ("question.wav", b"RIFFxxxx", "audio/wav")},
        )
        self.assertEqual(uploaded.status_code, 503)
        bad = self.client.post("/api/voice/ask", json={"audio_base64": "not base64!!!"})
        self.assertEqual(bad.status_code, 400)

    def test_garden_plan_form_without_speech(self):
        with patch(
            "agi_agent.gardening.voice.fetch_simple_forecast",
            return_value=_climate(),
        ), patch(
            "agi_agent.gardening.voice.geocode_location",
            return_value=(40.7128, -74.006),
        ):
            response = self.client.post(
                "/api/voice/garden-plan",
                data={
                    "text": "I want a small container garden of tomatoes",
                    "address": "New York, NY",
                },
            )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertIsNone(body["audio_base64"])
        self.assertFalse(body["speech_enabled"])
        self.assertIn("Tomatoes", body["plan"])
        self.assertEqual(body["parameter_source"], "keywords")

    def test_garden_plan_audio_without_a_key_is_disabled(self):
        response = self.client.post(
            "/api/voice/garden-plan",
            files={"audio_file": ("question.wav", b"RIFFxxxx", "audio/wav")},
        )
        self.assertEqual(response.status_code, 503)


class TestCommandLine(VoiceTestCase):
    def test_ask_and_status_and_transcribe(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = cli_main(["--ask", "What vegetables should I plant in spring?"])
        self.assertEqual(code, 0)
        self.assertIn("Lettuce", buffer.getvalue())

        buffer = StringIO()
        with redirect_stdout(buffer):
            code = cli_main(["--voice"])
        self.assertEqual(code, 0)
        self.assertIn("disabled", buffer.getvalue().lower())
        self.assertIn("DEEPGRAM_API_KEY", buffer.getvalue())

        buffer = StringIO()
        with redirect_stdout(buffer):
            code = cli_main(["--transcribe", "missing-audio.wav"])
        self.assertEqual(code, 2)
        self.assertIn("DEEPGRAM_API_KEY", buffer.getvalue())


class TestEnvExample(unittest.TestCase):
    def test_example_names_are_empty(self):
        with open(".env.example", encoding="utf-8") as handle:
            lines = [line.strip() for line in handle if line.strip()]
        self.assertEqual(
            lines,
            [
                "GOOGLE_MAPS_API_KEY=",
                "PORT=",
                "DEEPGRAM_API_KEY=",
                "OPENAI_API_KEY=",
            ],
        )
        for line in lines:
            name, value = line.split("=", 1)
            self.assertEqual(value, "")
            self.assertNotIn("sk-", name)


if __name__ == "__main__":
    unittest.main()
