"""
Memory module.
"""


from pymem.constants.defines import READ_PROCESS_MEMORY
from pymem.contrib.decorators import has_handle
from ctypes import create_string_buffer
from ctypes import c_ulong
from ctypes import byref
import struct


class Memory(object):
    """This Class provides the required functionalities to read and write
processes.
    """

    def __init__(self, h_process=None):
        """
        Memory constructor, you have to provide the handle of a process.
        """

        self._h_process = h_process
        self.is_process_set = self._h_process is not None
        self.read_types = {
            'float': self._read_float,
            'int': self._read_int,
            'uint': self._read_uint,
            'long': self._read_long,
            'ulong': self._read_ulong,
            'byte': self._read_bytes
        }

    def set_process(self, h_process):
        """
        Change or set current opened process
        """

        if h_process is not None:
            self._h_process = h_process
            self.is_process_set = True

    def read_offset(self, address, selected_type):
        """
        read memory from a process.
        If the type <T> is supported, this method will provide the required
        call in order to read, from the process. If either the type <T> is not
        supported or process is not Open, the method will raise an Exception.
        """

        try:
            if type(address) == list:
                ret = 0
                for addr in address:
                    ret = ret + addr
                    ret = self.read_types[selected_type](ret)
                    print ret
                return ret
            else:
                return self.read_types[selected_type](address)
        except KeyError:
            raise Exception("Unsuported type : %s" % selected_type)

    def _read_bytes(self, address, byte=4):
        """
        read bytes from a process, process has to be opened has usual.
        This method use ReadProcessMemory from kernel32.dll
        """

        buff = create_string_buffer(byte)
        bytes_read = c_ulong(0)
        buffer_size = byte
        READ_PROCESS_MEMORY(self._h_process, address, buff, \
        buffer_size, byref(bytes_read))
        string = buff.raw
        return string

    @has_handle()
    def _read_int(self, address):
        """
        read integer from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 4)
        number = struct.unpack('<i', string)[0]
        return number

    def _read_uint(self, address):
        """
        read unsigned int from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 4)
        number = struct.unpack('<I', string)[0]
        return number

    @has_handle()
    def _read_long(self, address):
        """
        read long from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 4)
        number = struct.unpack('<l', string)[0]
        return number

    @has_handle()
    def _read_ulong(self, address):
        """
        read unsigned long from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 4)
        number = struct.unpack('<L', string)[0]
        return number

    @has_handle()
    def _read_float(self, address):
        """
        read float from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 4)
        number = struct.unpack('<f', string)[0]
        return number
