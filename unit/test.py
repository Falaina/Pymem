import unittest
from pymem.core import Pymem


class TestPymemClass(unittest.TestCase):
    """TestPymemClass"""

    def setUp(self):
        self.pymem = Pymem()

    def test_open_from_name(self):
        self.assertTrue(self.pymem.open_process_from_name('explorer'))

    def test_open_from_id(self):
        self.assertTrue(self.pymem.open_process(2124))

    def test_read(self):
        self.pymem.open_process_from_name('Wow')
        pointer = self.pymem.read_offset([0xCD87A8 - 0x8, 0x34, 0x24],\
        'uint')
        self.assertNotEqual(self.pymem.read_offset(pointer + 0x798,\
        'float'), 0x0)

    def test_read_string(self):
        self.pymem.open_process_from_name('Wow')
        self.assertNotEqual(self.pymem.read_offset(0xC79D18 - 0x8, 'string'),\
        '')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPymemClass)
    testResult = unittest.TextTestRunner(verbosity=2).run(suite)
