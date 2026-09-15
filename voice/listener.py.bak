import math
import time
from array import array

import speech_recognition as sr

from config.constants import (
    VOICE_PHRASE_LIMIT,
    VOICE_TIMEOUT,
)
from config.states import AssistantState
from core import app_state
from core.logger import logger
from voice.language_manager import language_manager


class Listener:
    """Capture microphone input and recognize speech."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.5

        self._calibrated = False

        self.last_text = ""
        self.last_time = 0.0

        self.input_level = 0

        self.last_recognition_language = (
            language_manager.get_primary_language()
        )

    # =========================================================
    # LISTEN
    # =========================================================

    def listen(self, wake_mode=False):
        """
        Listen once and return recognized text.

        wake_mode=True:
            Use primary language only for wake-word detection.

        wake_mode=False:
            Use configured multilingual recognition behavior.
        """

        try:
            with self.microphone as source:

                # -------------------------------------------------
                # CALIBRATION
                # -------------------------------------------------

                if not self._calibrated:

                    logger.info(
                        "🎤 Calibrating microphone..."
                    )

                    self.recognizer.adjust_for_ambient_noise(
                        source,
                        duration=1,
                    )

                    self._calibrated = True

                    logger.info(
                        "✅ Calibration complete."
                    )

                # -------------------------------------------------
                # LISTENING
                # -------------------------------------------------

                app_state.state_machine.change(
                    AssistantState.LISTENING
                )

                logger.info(
                    "🎤 Listening..."
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=VOICE_TIMEOUT,
                    phrase_time_limit=VOICE_PHRASE_LIMIT,
                )

                self.input_level = (
                    self._calculate_audio_level(
                        audio
                    )
                )

            # -----------------------------------------------------
            # RECOGNITION
            # -----------------------------------------------------

            logger.info(
                "🧠 Recognizing..."
            )

            result = self._recognize_audio(
                audio,
                wake_mode=wake_mode,
            )

            audio = None

            if not result:
                return ""

            text, language = result

            text = text.strip().lower()

            if not text:
                return ""

            # -----------------------------------------------------
            # UPDATE DETECTED LANGUAGE
            # -----------------------------------------------------

            language_manager.set_detected_language(
                language
            )

            self.last_recognition_language = (
                language
            )

            logger.info(
                "Detected language: %s",
                language,
            )

            # -----------------------------------------------------
            # DUPLICATE PROTECTION
            # -----------------------------------------------------

            now = time.time()

            if (
                text == self.last_text
                and (
                    now
                    - self.last_time
                ) < 2.5
            ):

                logger.info(
                    "🔁 Duplicate command ignored: %s",
                    text,
                )

                return ""

            self.last_text = text
            self.last_time = now

            logger.info(
                "Recognized [%s]: %s",
                language,
                text,
            )

            return text

        # =========================================================
        # TIMEOUT
        # =========================================================

        except sr.WaitTimeoutError:
            return ""

        # =========================================================
        # UNKNOWN SPEECH
        # =========================================================

        except sr.UnknownValueError:
            return ""

        # =========================================================
        # RECOGNITION SERVICE
        # =========================================================

        except sr.RequestError as error:

            logger.error(
                "Speech recognition service error: %s",
                error,
            )

            return ""

        # =========================================================
        # MICROPHONE
        # =========================================================

        except OSError as error:

            logger.exception(
                "Microphone error: %s",
                error,
            )

            return ""

        # =========================================================
        # OTHER
        # =========================================================

        except Exception as error:

            logger.exception(
                "Listener error: %s",
                error,
            )

            return ""

    # =========================================================
    # RECOGNITION
    # =========================================================

    def _recognize_audio(
        self,
        audio,
        wake_mode=False,
    ):
        """
        Recognize speech.

        Wake mode:
            Primary language only.

        Normal mode:
            Manual primary language or multilingual detection.
        """

        # =========================================================
        # WAKE WORD MODE
        # =========================================================

        if wake_mode:

            language = (
                language_manager.get_primary_language()
            )

            code = (
                language_manager.recognition_code()
            )

            logger.info(
                "Wake-word recognition language: %s (%s)",
                language,
                code,
            )

            text = self._recognize_with_code(
                audio,
                code,
            )

            if not text:
                return None

            return (
                text,
                language,
            )

        # =========================================================
        # MANUAL LANGUAGE MODE
        # =========================================================

        if not language_manager.is_auto_detect():

            language = (
                language_manager.get_primary_language()
            )

            code = (
                language_manager.recognition_code()
            )

            logger.info(
                "Recognition language: %s (%s)",
                language,
                code,
            )

            text = self._recognize_with_code(
                audio,
                code,
            )

            if not text:
                return None

            return (
                text,
                language,
            )

        # =========================================================
        # AUTOMATIC LANGUAGE MODE
        # =========================================================

        codes = (
            self._get_unique_recognition_codes()
        )

        if not codes:
            codes = [
                language_manager.recognition_code()
            ]

        primary_code = (
            language_manager.recognition_code()
        )

        ordered_codes = []

        # Primary language first.
        if primary_code in codes:
            ordered_codes.append(
                primary_code
            )

        for code in codes:

            if code not in ordered_codes:
                ordered_codes.append(
                    code
                )

        candidates = []

        for code in ordered_codes:

            try:

                candidate = (
                    self._recognize_with_details(
                        audio,
                        code,
                    )
                )

                if candidate is None:
                    continue

                text = candidate.get(
                    "text",
                    "",
                ).strip()

                if not text:
                    continue

                confidence = candidate.get(
                    "confidence"
                )

                candidates.append(
                    {
                        "text": text,
                        "code": code,
                        "confidence": confidence,
                    }
                )

                logger.info(
                    "Recognition candidate [%s]: %s",
                    code,
                    text,
                )

            except sr.UnknownValueError:
                continue

            except sr.RequestError:
                raise

            except Exception as error:

                logger.warning(
                    "Recognition failed for %s: %s",
                    code,
                    error,
                )

        if not candidates:
            return None

        # =========================================================
        # LANGUAGE-AWARE CANDIDATE SCORING
        # =========================================================

        primary_language = (
            language_manager.get_primary_language()
        )

        scored_candidates = []

        for candidate in candidates:

            text = candidate["text"]
            code = candidate["code"]

            score = 0.0

            # -------------------------------------------------
            # SCRIPT-BASED LANGUAGE MATCH
            # -------------------------------------------------

            script = self._detect_script(
                text
            )

            if script == "latin":

                if code == "en-US":
                    score += 70

                elif code == "ur-PK":

                    # Roman Urdu uses Latin script.
                    if primary_language == "Roman Urdu":
                        score += 65
                    else:
                        score += 10

            elif script == "urdu":

                if code == "ur-PK":
                    score += 70
                else:
                    score -= 30

            elif script == "gurmukhi":

                if code == "pa-IN":
                    score += 70
                else:
                    score -= 30

            elif script == "devanagari":

                if code == "hi-IN":
                    score += 70
                else:
                    score -= 30

            # -------------------------------------------------
            # PRIMARY LANGUAGE
            # -------------------------------------------------

            if (
                primary_language == "English"
                and code == "en-US"
            ):
                score += 30

            elif (
                primary_language in {
                    "Urdu",
                    "Roman Urdu",
                }
                and code == "ur-PK"
            ):
                score += 30

            elif (
                primary_language == "Punjabi"
                and code == "pa-IN"
            ):
                score += 30

            elif (
                primary_language == "Hindi"
                and code == "hi-IN"
            ):
                score += 30

            # -------------------------------------------------
            # BACKEND CONFIDENCE
            #
            # Use confidence only as a small tie-breaker.
            # It should NOT dominate script detection.
            # -------------------------------------------------

            confidence = candidate.get(
                "confidence"
            )

            if isinstance(
                confidence,
                (int, float),
            ):
                score += min(
                    float(confidence) * 10,
                    10,
                )

            candidate["score"] = score

            scored_candidates.append(
                candidate
            )

            logger.info(
                "Candidate score [%s]: %.2f | %s",
                code,
                score,
                text,
            )

        # ---------------------------------------------------------
        # SELECT BEST CANDIDATE
        # ---------------------------------------------------------

        best = max(
            scored_candidates,
            key=lambda item: item["score"],
        )

        language = (
            language_manager.language_for_code(
                best["code"]
            )
        )

        # Roman Urdu uses Urdu recognition.
        if (
            primary_language == "Roman Urdu"
            and best["code"] == "ur-PK"
        ):
            language = "Roman Urdu"

        logger.info(
            "Selected candidate [%s] score=%.2f: %s",
            best["code"],
            best["score"],
            best["text"],
        )

        return (
            best["text"],
            language,
        )

    # =========================================================
    # SCRIPT DETECTION
    # =========================================================

    @staticmethod
    def _detect_script(text):
        """Detect the dominant writing system."""

        latin = 0
        urdu = 0
        gurmukhi = 0
        devanagari = 0

        for char in text:

            codepoint = ord(char)

            # Basic Latin letters.
            if (
                0x0041
                <= codepoint
                <= 0x007A
            ):
                latin += 1

            # Arabic / Urdu.
            elif (
                0x0600
                <= codepoint
                <= 0x06FF
            ):
                urdu += 1

            # Gurmukhi / Punjabi.
            elif (
                0x0A00
                <= codepoint
                <= 0x0A7F
            ):
                gurmukhi += 1

            # Devanagari / Hindi.
            elif (
                0x0900
                <= codepoint
                <= 0x097F
            ):
                devanagari += 1

        counts = {
            "latin": latin,
            "urdu": urdu,
            "gurmukhi": gurmukhi,
            "devanagari": devanagari,
        }

        script, count = max(
            counts.items(),
            key=lambda item: item[1],
        )

        if count == 0:
            return "unknown"

        return script

    # =========================================================
    # RECOGNIZE WITH CODE
    # =========================================================

    def _recognize_with_code(
        self,
        audio,
        code,
    ):
        """Recognize audio using one language code."""

        return (
            self.recognizer.recognize_google(
                audio,
                language=code,
            )
        )

    # =========================================================
    # RECOGNIZE WITH DETAILS
    # =========================================================

    def _recognize_with_details(
        self,
        audio,
        code,
    ):
        """Return transcript and optional confidence."""

        response = (
            self.recognizer.recognize_google(
                audio,
                language=code,
                show_all=True,
            )
        )

        if not response:
            return None

        if isinstance(
            response,
            dict,
        ):

            alternatives = response.get(
                "alternative",
                [],
            )

            if not alternatives:
                return None

            best = alternatives[0]

            return {
                "text": best.get(
                    "transcript",
                    "",
                ),
                "confidence": best.get(
                    "confidence"
                ),
            }

        if isinstance(
            response,
            str,
        ):

            return {
                "text": response,
                "confidence": None,
            }

        return None

    # =========================================================
    # UNIQUE RECOGNITION CODES
    # =========================================================

    @staticmethod
    def _get_unique_recognition_codes():
        """Get unique enabled speech-recognition codes."""

        codes = (
            language_manager.enabled_recognition_codes()
        )

        unique = []

        for code in codes:

            if code not in unique:
                unique.append(code)

        return unique

    # =========================================================
    # AUDIO LEVEL
    # =========================================================

    @staticmethod
    def _calculate_audio_level(audio):
        """Estimate RMS level of captured audio."""

        raw = audio.get_raw_data()

        if not raw:
            return 0

        width = audio.sample_width

        try:

            if width == 1:

                samples = array(
                    "B",
                    raw,
                )

                if not samples:
                    return 0

                values = [
                    sample - 128
                    for sample in samples
                ]

                max_amplitude = 128

            elif width == 2:

                samples = array(
                    "h"
                )

                samples.frombytes(
                    raw
                )

                if not samples:
                    return 0

                values = samples
                max_amplitude = 32768

            elif width == 4:

                samples = array(
                    "i"
                )

                samples.frombytes(
                    raw
                )

                if not samples:
                    return 0

                values = samples
                max_amplitude = 2147483648

            else:
                return 0

            mean_square = sum(
                sample * sample
                for sample in values
            ) / len(values)

            rms = math.sqrt(
                mean_square
            )

            # Amplify normalized RMS into a useful 0-100 range.
            level = (
                rms
                / max_amplitude
                * 100
                * 10
            )

            return int(
                max(
                    0,
                    min(
                        level,
                        100,
                    ),
                )
            )

        except Exception:
            return 0