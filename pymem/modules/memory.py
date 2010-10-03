"""
Memory module.
"""


from pymem.constants.defines import READ_PROCESS_MEMORY
from pymem.contrib.decorators import has_handle
from ctypes import create_string_buffer
from ctypes import c_ulong, c_float, c_char_p, c_ulonglong
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
            'uint': self._read_uint,
            'int': self._read_int,
            'long': self._read_long,
            'ulong': self._read_ulong,
            'int64': self._read_int64,
            'uint64': self._read_uint64,
            'byte': self._read_bytes,
            'string': self._read_string,
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
                ret = self.read_types[selected_type](address[0])
                for addr in address[1:]:
                    ret = self.read_types[selected_type](ret + addr)
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
        return buff.raw

    @has_handle()
    def _read_int(self, address):
        """
        read integer from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 4)
        number = struct.unpack('<i', string)[0]
        return number

    @has_handle()
    def _read_uint(self, address):
        """
        read unsigned int from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 4)
        number = struct.unpack('<I', string)[0]
        return number

    @has_handle()
    def _read_int64(self, address):
        """
        read unsigned int from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 8) #int64 is twice as big as a normal int (ie c_ulonglong)
        number = struct.unpack('<q', string)[0]
        return number
        
    @has_handle()
    def _read_uint64(self, address):
        """
        read unsigned int from a process, process has to be opened has usual.
        This method use readBytes.
        """

        string = self._read_bytes(address, 8) #int64 is twice as big as a normal int (ie c_ulonglong)
        number = struct.unpack('<Q', string)[0]
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

    @has_handle()
    def _read_string(self, address, byte=50):
        """
        read string from a process, process has to be opened has usual.
        This method use readBytes.

        __usage__	name = m.readString(0x000000)
        """

        buff = self._read_bytes(address, byte)
        i = buff.find('\x00')
        if i != -1:
            return buff[:i]
        else:
            return buff
            
  #------ Memory writing ------#
    
  #@param address   memory address to write
  #@param data      information to write
  #@return  True if successful (no error)
  @hasHandle
  def _write_offset(self, address, data):
    
    #Choose type letter for struct.pack
    typeDict = { type(int()):'i', 
                 #type(uint()):'I', 
                 type(float()):'f',
                 #type(int64()):'',
                 type(long()):'Q', #int64/uint64, here assuming uint64
                 type(str()):'s',
               }
    typeLetter = typeDict[type(data)]
    
    #Choose 5th argument for WriteProcessMemory
    refDict = { type(int()):c_int(0), 
            type(float()):c_float(0.),
            type(str()):c_char_p(str(data)),
            #type(uint()):c_uint(data), #uint() doesn't exist in python
            #type(int64()):c_ulonglong(data), #int64/uint64 does not exist in python, look for long() which is anything bigger than int()
            type(long()):c_ulonglong(0), #int64/uint64
          }

    c_data = struct.pack(typeLetter,data)
    length = struct.calcsize(typeLetter)
    if type(data)==type(str): length = len(data) #or len(data)*4? #@Not tested, likely wrong
    windll.kernel32.SetLastError(10000)
    if not windll.kernel32.WriteProcessMemory(self._h_process, address, c_data, length, byref(refDict[type(data)])):
        print "Failed to write memory."
        print  "Error Code: ",windll.kernel32.GetLastError()
    else:
        return True  
