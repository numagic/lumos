from re import L
import unittest

from lumos.optimal_control.transcription import (
    get_transcription_options,
    make_transcription,
    ForwardEuler,
    Trapezoidal,
    LGR,
    LGRIntegral,
)


class TestMakeTranscription(unittest.TestCase):
    def test_make_LGR(self):
        transcription = make_transcription("LGR", {"num_stages": 3})
        self.assertIsInstance(transcription, LGR)
        self.assertEqual(transcription.num_stages_per_interval, 3)

    def test_make_ForwardEuler(self):
        transcription = make_transcription("ForwardEuler")
        self.assertIsInstance(transcription, ForwardEuler)
        self.assertEqual(transcription.num_stages_per_interval, 2)

    def test_make_Trapezoidal(self):
        transcription = make_transcription("Trapezoidal")
        self.assertIsInstance(transcription, Trapezoidal)
        self.assertEqual(transcription.num_stages_per_interval, 2)

    def test_make_LGRIntegral(self):
        transcription = make_transcription("LGRIntegral", {"num_stages": 5})
        self.assertIsInstance(transcription, LGRIntegral)
        self.assertEqual(transcription.num_stages_per_interval, 5)

    def test_make_something_wrong(self):
        # Type not supported
        with self.assertRaises(RuntimeError):
            transcription = make_transcription("LGL")

        # Unwanted input arguments, the constructor should raise TypeError
        with self.assertRaises(TypeError):
            transcription = make_transcription("ForwardEuler", {"someargs": 1.0})

    def test_get_and_make_transcriptions(self):
        options = get_transcription_options()

        for name in options:
            transcription = make_transcription(name)
            self.assertEqual(transcription.__class__.__name__, name)


class TestTranscription(unittest.TestCase):
    @unittest.skip("To be implemented")
    def test_continuity_transcription(self):
        """Test if the transcription of a continuous time system is accurate."""
        raise NotImplementedError
