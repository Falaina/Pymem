# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <nopz> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Nopz
# ----------------------------------------------------------------------------

from decorator import hasHandle
from ctypes import create_string_buffer, c_ulong, byref, c_int, c_uint, c_ulonglong, c_float, c_char_p,windll
import struct

class Memory(object):
  """
  This Class provides the required functionalities to read and write
  processes.
  """
  
  def __init__(self, h_process = None):
    """
    Memory constructor, you have to provide the handle of a process.
    
    __usage__	p = Process()
          p.open_process_debug(e[0].th32ProcessID)
          m = Memory(p.h_process)
    """

    self._h_process = h_process
    self.isProcessSet = self._h_process is not None
    self.readTypes = {
      'float' : self.readFloat,
      'int' : self.readInt,
      'uint' : self.readUInt,
      'uint64' : self.readUInt64,
      'long' : self.readLong,
      'ulong' : self.readInt,
      'byte' : self.readBytes
    }
  
  def setProcess(self, h_process):
    """
    Change or set current opened process
    
    __usage__	m.SetProcess(h_process)
    """
    
    self._h_process = h_process
    self.isProcessSet = self._h_process is not None

  @hasHandle
  def readOffset(self, address, T):
    """
    read memory from a process.
    If the type <T> is supported, this method will provide the required
    call in order to read, from the process. If either the type <T> is not
    supported or process is not Open, the method will raise an Exception.
    
    __usage__	playerBase = m.readOffset([0xCF8C50, 0x34, 0x24], 'uint')
          player_x = m.readOffset(playerBase + 0x798, 'float')
    """

    try:
      if type(address) == list:
        ret = 0
        for a in address:
          ret = ret + a
          ret = self.readTypes[T](ret)
        return ret
      else:
        return self.readTypes[T](address)
    except KeyError:
      raise Exception("Unsuported type : %s" % T)
  
    
  #@param address   memory address to write
  #@param data      information to write
  #@return  True if successful (no error)
  @hasHandle
  def write_memory(self, address, data):
    
    #Choose type letter for struct.pack
    typeDict = { type(int()):'i', 
                 #type(uint()):'I', 
                 type(float()):'f',
                 #type(int64()):'',
                 type(long()):'Q', #uint64
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

    #PROCESS_ALL_ACCESS = 0x001F0FFF #Is this required for Vista/Win7? It is not currently used, and if needed should be more specific than all_access
    c_data = struct.pack(typeLetter,data)
    length = struct.calcsize(typeLetter)
    if type(data)==type(str): length = len(data) #or len(data)*4? #@Not tested
    windll.kernel32.SetLastError(10000)
    if not windll.kernel32.WriteProcessMemory(self._h_process, address, c_data, length, byref(refDict[type(data)])):
        print "Failed to write memory."
        print  "Error Code: ",windll.kernel32.GetLastError()
    else:
        return True  
    
  @hasHandle
  def readBytes(self, address, bytes=4):
    """
    read bytes from a process, process has to be opened has usual.
    This method use ReadProcessMemory from kernel32.dll
    for more define information -> Memory/defines.py
    
    __usage__	byte_value = m.readOffset(0x000000, 'float')
    """
    
    from Memory.defines import ReadProcessMemory
    
    buffer = create_string_buffer(bytes)
    bytesread = c_ulong(0) #what is this? should this become c_ulonglong(0) for int64?
    bufferSize = bytes
    ReadProcessMemory(self._h_process, address, buffer,\
    bufferSize,byref(bytesread))
    string = buffer.raw
    return string  
    
  @hasHandle
  def readBytes64(self, address, bytes=8):
    """
    read bytes from a process, process has to be opened has usual.
    This method use ReadProcessMemory from kernel32.dll
    for more define information -> Memory/defines.py
    
    __usage__	byte_value = m.readOffset(0x000000, 'float')
    """
    
    from Memory.defines import ReadProcessMemory
    
    buffer = create_string_buffer(bytes) # <----- This is the problem
    bytesread = c_ulonglong(0) #what is this? should this become c_ulonglong(0) for int64?
    bufferSize = bytes
    ReadProcessMemory(self._h_process, address, buffer,bufferSize,byref(bytesread))
    string = buffer.raw
    return string
  
  @hasHandle
  def readInt(self, address):
    """
    read integer from a process, process has to be opened has usual.
    This method use readBytes.
    
    __usage__	int_value = m.readInt(0x000000)
    """
    
    string = self.readBytes(address,4)
    number = struct.unpack('<i',string)[0]
    return number
  
  @hasHandle
  def readUInt(self, address):
    """
    read unsigned int from a process, process has to be opened has usual.
    This method use readBytes.
    
    __usage__	uint_value = m.readUInt(0x000000)
    """
    
    string = self.readBytes(address,4)
    number = struct.unpack('<I',string)[0]
    return number 
    
  @hasHandle
  def readUInt64(self, address):
    """
    read unsigned int from a process, process has to be opened has usual.
    This method use readBytes.
    
    __usage__	uint_value = m.readUInt(0x000000)
    """
    
    string = self.readBytes64(address,8)
    number = struct.unpack('Q',string)[0]
    return number

  @hasHandle
  def readLong(self, address):
    """
    read long from a process, process has to be opened has usual.
    This method use readBytes.
    
    __usage__	long_value = m.readLong(0x000000)
    """
    string = self.readBytes(address,4)
    number = struct.unpack('<l',string)[0]
    return number

  @hasHandle
  def readULong(self, address):
    """
    read unsigned long from a process, process has to be opened has usual.
    This method use readBytes.
    
    __usage__	ulong_value = m.readULong(0x000000)
    """
    string = self.readBytes(address,4)
    number = struct.unpack('<L',string)[0]
    return number

  @hasHandle
  def readFloat(self, address):
    """
    read float from a process, process has to be opened has usual.
    This method use readBytes.
    
    __usage__	float_value = m.readFloat(0x000000)
    """
    string = self.readBytes(address,4)
    number = struct.unpack('<f',string)[0]
    return number
    
  def readString(self, address, bytes=50):
    """
    read string from a process, process has to be opened has usual.
    This method use readBytes.
    
    __usage__	name = m.readString(0x000000)
    """
    
    buffer = self.readBytes(address, bytes)
    i = buffer.find('\x00')
    if i != -1:
      return buffer[:i]
    else:
      return buffer