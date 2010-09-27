"""
Ctype function defines
"""

from ctypes import c_int, c_void_p, c_long
from ctypes import windll, POINTER, wintypes
from pymem.constants.structures import PROCESSENTRY32

PROCESS_32_FIRST = windll.kernel32.Process32First
PROCESS_32_FIRST.argtypes = [c_void_p, POINTER(PROCESSENTRY32)]
PROCESS_32_FIRST.rettype = c_int

PROCESS_32_NEXT = windll.kernel32.Process32Next
PROCESS_32_NEXT.argtypes = [c_void_p, POINTER(PROCESSENTRY32)]
PROCESS_32_NEXT.rettype = c_int

CREATETOOLHELP_32_SNAPSHOT = windll.kernel32.CreateToolhelp32Snapshot
CREATETOOLHELP_32_SNAPSHOT.reltype = c_long
CREATETOOLHELP_32_SNAPSHOT.argtypes = [c_int, c_int]

CLOSE_HANDLE = windll.kernel32.CloseHandle
CLOSE_HANDLE.argtypes = [c_void_p]
CLOSE_HANDLE.rettype = c_int

OPEN_PROCESS = windll.kernel32.OpenProcess
OPEN_PROCESS.argtypes = [c_void_p, c_int, c_long]
OPEN_PROCESS.rettype = c_long

OPEN_PROCESS_TOKEN = windll.advapi32.OpenProcessToken
OPEN_PROCESS_TOKEN.argtypes = (wintypes.HANDLE, wintypes.DWORD, \
POINTER(wintypes.HANDLE))
OPEN_PROCESS_TOKEN.restype = wintypes.BOOL
