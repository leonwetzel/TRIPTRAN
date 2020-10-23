import unittest
from rdf import Triple


class TestRdf(unittest.TestCase):

    def test_init(self):
        """
        Test for the initialisation of Triple objects.
        :return:
        """
        with self.assertRaises(ValueError):
            _ = Triple()

    def test_str(self):
        triple = Triple("Durk", "eats", "cheese")
        self.assertEqual(str(triple), "Durk eats cheese")


if __name__ == '__main__':
    unittest.main()