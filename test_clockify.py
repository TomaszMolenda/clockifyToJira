import unittest

from clockify import ClokifyEntry


class AppTestCase(unittest.TestCase):
    def test_get_description_empty_from_clockify(self):
        entry = ClokifyEntry("XXXX-1111")
        description = entry.get_description()
        self.assertEqual(description, '')

    def test_get_description_from_clockify(self):
        entry = ClokifyEntry("XXXX-1111 bla blabla")
        description = entry.get_description()
        self.assertEqual(description, 'bla blabla')


if __name__ == '__main__':
    unittest.main()
