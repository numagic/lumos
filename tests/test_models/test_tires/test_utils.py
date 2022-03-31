from unittest import TestCase
from lumos.models.tires.utils import read_tir_file


class TestReadTirFile(TestCase):
    def test_read(self):
        """Read the default file and assert the contents"""

        # TODO: we need better management of test data
        params = read_tir_file("data/tires/default.tir")

        # Check if all read items are floats
        self.assertTrue(all([isinstance(v, float) for v in params.values()]))

        # Check if some selected float items are correctly read
        self.assertAlmostEqual(params["PCX1"], 1.3605)
        self.assertAlmostEqual(params["PEX2"], -0.475)

        # Check if non-float items are not read
        self.assertRaises(KeyError, lambda: params["FILE_TYPE"])
        self.assertRaises(KeyError, lambda: params["PROPERTY_FILE_FORMAT"])
