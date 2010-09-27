import unittest
from pymem.pymem import Pymem


class TestPymemClass(unittest.TestCase):
    """TestPymemClass"""

    def setUp(self):
        self.pymem = Pymem()

    def test_open_from_name(self):
        self.assertTrue(self.pymem.open_process_from_name('explorer'))

    def test_open_from_id(self):
        self.assertTrue(self.pymem.open_process(2124))

if __name__ == '__main__':
    unittest.main()
