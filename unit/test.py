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
        
    def test_read(self):
        PLAYER_BASE = 0xCD87A8
        PLAYER_BASE_OFFSET1 = 0x34
        PLAYER_BASE_OFFSET2 = 0x24
        print self.pymem.open_process_from_name('Wow')
        pointer = self.pymem.read_offset([PLAYER_BASE, PLAYER_BASE_OFFSET1, PLAYER_BASE_OFFSET2], 'uint')
        print pointer
        print self.pymem.read_offset(pointer + 0x798, 'float')
        

if __name__ == '__main__':
    unittest.main()
