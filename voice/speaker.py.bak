import asyncio
from io import BytesIO

import av
import edge_tts
import numpy as np
import pyttsx3
import sounddevice as sd

from config.languages import LANGUAGES
from voice.language_manager import language_manager


class Speaker:
    """
    JARVIS multilingual text-to-speech router.

    English:
        Windows SAPI5

    Urdu:
        Microsoft Edge TTS

    Roman Urdu:
        Microsoft Edge Urdu TTS

    Hindi:
        Microsoft Edge TTS

    Punjabi:
        Urdu neural voice fallback until a native Punjabi
        voice is available.
    """

    EDGE_VOICES = {
        "Urdu": "ur-PK-AsadNeural",
        "Roman Urdu": "ur-PK-AsadNeural",
        "Hindi": "hi-IN-MadhurNeural",
        "Punjabi": None,
    }

    SAPI_LANGUAGES = {
        "English",
    }

    def speak(
        self,
        text,
        language=None,
    ):
        if not text:
            return

        # ---------------------------------------------------------
        # RESPONSE LANGUAGE
        # ---------------------------------------------------------

        if language is None:

            language = (
                language_manager
                .get_response_language()
            )

        print(
            "Requested speech language:",
            language,
        )

        # ---------------------------------------------------------
        # ENGLISH → SAPI5
        # ---------------------------------------------------------

        if language in self.SAPI_LANGUAGES:

            try:

                self._speak_sapi(
                    text,
                    language,
                )

                return

            except Exception as error:

                print(
                    "SAPI5 speech failed:",
                    error,
                )

                # Fall back to Edge English if possible.
                try:

                    self._speak_edge(
                        text,
                        "en-US-AndrewNeural",
                    )

                    return

                except Exception as edge_error:

                    print(
                        "Edge English fallback failed:",
                        edge_error,
                    )

                return

        # ---------------------------------------------------------
        # MULTILINGUAL EDGE TTS
        # ---------------------------------------------------------

        edge_voice = (
            self.EDGE_VOICES.get(
                language
            )
        )
        
        if not edge_voice:
        
            print(
                "No compatible TTS voice configured for:",
                language,
            )
        
            return

        try:

            self._speak_edge(
                text,
                edge_voice,
            )

        except Exception as error:

            print(
                "Edge TTS failed:",
                error,
            )

            # Final fallback to SAPI.
            try:

                self._speak_sapi(
                    text,
                    "English",
                )

            except Exception as fallback_error:

                print(
                    "Final TTS fallback failed:",
                    fallback_error,
                )

    # =========================================================
    # SAPI5
    # =========================================================

    def _speak_sapi(
        self,
        text,
        language,
    ):
        print(
            "Creating SAPI5 engine..."
        )

        engine = pyttsx3.init(
            "sapi5"
        )

        voices = (
            engine.getProperty(
                "voices"
            )
        )

        selected_voice = None

        language_codes = (
            LANGUAGES.get(
                language,
                {},
            ).get(
                "speech_codes",
                ["en-US"],
            )
        )

        # ---------------------------------------------------------
        # SEARCH MATCHING VOICE
        # ---------------------------------------------------------

        for voice in voices:

            voice_languages = (
                getattr(
                    voice,
                    "languages",
                    [],
                )
            )

            voice_data = (
                str(
                    voice_languages
                ).lower()
            )

            voice_name = (
                str(
                    getattr(
                        voice,
                        "name",
                        "",
                    )
                ).lower()
            )

            voice_id = (
                str(
                    getattr(
                        voice,
                        "id",
                        "",
                    )
                ).lower()
            )

            for code in language_codes:

                normalized_code = (
                    code.lower()
                    .replace(
                        "-",
                        "",
                    )
                    .replace(
                        "_",
                        "",
                    )
                    .replace(
                        " ",
                        "",
                    )
                )

                normalized_voice_data = (
                    voice_data
                    .replace(
                        "-",
                        "",
                    )
                    .replace(
                        "_",
                        "",
                    )
                    .replace(
                        " ",
                        "",
                    )
                )

                if (
                    normalized_code
                    in normalized_voice_data
                ):

                    selected_voice = voice
                    break

                short_code = (
                    normalized_code[:2]
                )

                if (
                    short_code
                    and short_code
                    in voice_name
                ):

                    selected_voice = voice
                    break

                if (
                    short_code
                    and short_code
                    in voice_id
                ):

                    selected_voice = voice
                    break

            if selected_voice:
                break

        # ---------------------------------------------------------
        # FALLBACK
        # ---------------------------------------------------------

        if (
            selected_voice is None
            and voices
        ):

            selected_voice = voices[0]

            print(
                "No language-matched SAPI voice found."
            )

        # ---------------------------------------------------------
        # APPLY
        # ---------------------------------------------------------

        if selected_voice is not None:

            engine.setProperty(
                "voice",
                selected_voice.id,
            )

            print(
                "Selected SAPI voice:",
                selected_voice.name,
            )

        engine.setProperty(
            "rate",
            175,
        )

        engine.setProperty(
            "volume",
            1.0,
        )

        print(
            "Speaking:",
            text,
        )

        engine.say(
            text
        )

        engine.runAndWait()

        engine.stop()

        print(
            "SAPI5 finished."
        )

    # =========================================================
    # EDGE TTS
    # =========================================================

    def _speak_edge(
        self,
        text,
        voice,
    ):
        print(
            "Creating Edge TTS:",
            voice,
        )

        audio_data = asyncio.run(
            self._generate_edge_audio(
                text,
                voice,
            )
        )

        if not audio_data:
            raise RuntimeError(
                "Edge TTS returned no audio."
            )

        samples, sample_rate = (
            self._decode_mp3(
                audio_data
            )
        )

        if samples.size == 0:
            raise RuntimeError(
                "Decoded Edge TTS audio is empty."
            )

        print(
            "Playing Edge TTS:",
            voice,
        )

        sd.play(
            samples,
            sample_rate,
        )

        sd.wait()

        print(
            "Edge TTS finished."
        )

    # =========================================================
    # EDGE AUDIO GENERATION
    # =========================================================

    @staticmethod
    async def _generate_edge_audio(
        text,
        voice,
    ):
        communicate = (
            edge_tts.Communicate(
                text,
                voice,
            )
        )

        chunks = []

        async for chunk in (
            communicate.stream()
        ):

            if (
                chunk.get("type")
                == "audio"
            ):

                data = chunk.get(
                    "data"
                )

                if data:
                    chunks.append(
                        data
                    )

        return b"".join(
            chunks
        )

    # =========================================================
    # MP3 DECODER
    # =========================================================

    @staticmethod
    def _decode_mp3(
        audio_data,
    ):
        container = av.open(
            BytesIO(
                audio_data
            ),
            format="mp3",
        )

        frames = []

        sample_rate = 24000

        try:

            for frame in (
                container.decode(
                    audio=0
                )
            ):

                sample_rate = (
                    frame.sample_rate
                    or sample_rate
                )

                array = frame.to_ndarray()

                frames.append(
                    array
                )

        finally:

            container.close()

        if not frames:

            return (
                np.array(
                    [],
                    dtype=np.float32,
                ),
                sample_rate,
            )

        audio = np.concatenate(
            frames,
            axis=1,
        )

        # ---------------------------------------------------------
        # Convert:
        # (channels, samples)
        # →
        # (samples, channels)
        # ---------------------------------------------------------

        audio = audio.T

        # ---------------------------------------------------------
        # Normalize integer PCM.
        # ---------------------------------------------------------

        if np.issubdtype(
            audio.dtype,
            np.integer,
        ):

            info = np.iinfo(
                audio.dtype
            )

            max_value = max(
                abs(info.min),
                info.max,
            )

            audio = (
                audio.astype(
                    np.float32
                )
                / max_value
            )

        else:

            audio = audio.astype(
                np.float32
            )

        # ---------------------------------------------------------
        # Mono cleanup.
        # ---------------------------------------------------------

        if audio.ndim == 1:

            return (
                audio,
                sample_rate,
            )

        if (
            audio.ndim == 2
            and audio.shape[1] == 1
        ):

            return (
                audio[:, 0],
                sample_rate,
            )

        return (
            audio,
            sample_rate,
        )