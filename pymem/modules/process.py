"""
Process module.
"""

from ctypes import pointer
from ctypes import sizeof
from pymem.constants.structures import PROCESS_CLASS
from pymem.constants.defines import PROCESS_32_FIRST
from pymem.constants.defines import PROCESS_32_NEXT
from pymem.constants.defines import CREATETOOLHELP_32_SNAPSHOT
from pymem.constants.defines import CLOSE_HANDLE
from pymem.constants.defines import OPEN_PROCESS
from pymem.constants.structures import PROCESSENTRY32
from pymem.constants.structures import TH32CS_CLASS
from win32api import GetCurrentProcess
from win32security import GetSecurityInfo
from win32security import SetSecurityInfo

import win32security
import copy


class Process(object):
    """Process class.
The aim of this Class is to provide the required functionalities regarding
processes, including debugging.
    """

    def __init__(self):
        """
        __usage__	p = Process()
        """

        self.h_process = None
        self.pid = None
        self.is_process_open = False
        self.process32 = None

    def __del__(self):
        """
        Will close the handle if we have something opened.
        """

        self.close()

    def open(self, dw_process_id, process_access=PROCESS_CLASS.ALL):
        """
        Open a process from its dw_process_id with the desired access

        __usage__	wow_process = p.open(8992, PROCESS_CLASS.ALL)
        """

        self.h_process = OPEN_PROCESS(process_access, 0, dw_process_id)
        if self.h_process is not None:
            self.is_process_open = True
            self.process32 = process32_from_id(dw_process_id)
            return True
        return False

    def open_debug(self, dw_process_id):
        """
        Open a process from its dwProcessId with the desired access
        This function put the process into debug mode, wich allows to
        read/write memory.
        This method first grab security information from  the curent process,
        then we open the specified process with previous security information.

        __usage__	wow_process = p.open(8992, PROCESS_CLASS.ALL)
        """

        process = OPEN_PROCESS(0x00040000, 0, dw_process_id)
        info = GetSecurityInfo(GetCurrentProcess(), 6, 0)
        SetSecurityInfo(process, 6, \
                    win32security.DACL_SECURITY_INFORMATION |\
                    win32security.UNPROTECTED_DACL_SECURITY_INFORMATION,\
                    None,\
                    None,\
                    info.GetSecurityDescriptorDacl(),\
                    info.GetSecurityDescriptorGroup())
        CLOSE_HANDLE(process)
        self.h_process = OPEN_PROCESS(PROCESS_CLASS.ALL, 0, dw_process_id)
        if self.h_process:
            self.is_process_open = True
            self.process32 = process32_from_id(dw_process_id)
            return True
        return False

    def close(self):
        """
        Close a process handle

        __usage__	p.close()
        """

        if self.h_process is not None:
            ret = CLOSE_HANDLE(self.h_process) == 1
            if ret:
                self.h_process = None
                self.pid = None
                self.is_process_open = False
                self.process32 = None
            return ret
        return False


def process_list():
    """
    This function return a list <PROCESSENTRY32> containing all available
    processes.

    __usage__	process_list = process_list()
    """

    processes = []
    h_process_snap = CREATETOOLHELP_32_SNAPSHOT(\
        TH32CS_CLASS.SNAPPROCESS, 0)
    pe32 = PROCESSENTRY32()
    pe32.dwSize = sizeof(PROCESSENTRY32)
    ret = PROCESS_32_FIRST(h_process_snap, pointer(pe32))
    while ret:
        ret = PROCESS_32_NEXT(h_process_snap, pointer(pe32))
        if pe32.dwFlags == 0:
            processes.append(copy.copy(pe32))
        else:
            break
    CLOSE_HANDLE(h_process_snap)
    return processes


def process32_from_id(dw_process_id):
    """
    Return a Process fron its process id.
    """

    p_list = process_list()
    for process in p_list:
        if process.th32ProcessID == dw_process_id:
            return process
    return None


def name_from_process(dw_process_id):
    """
    From a processId will return the process exe Name or False is process
    is not found.

    __usage__	wow_pids = name_from_process(1337)
    """

    p_list = process_list()
    for process in p_list:
        if process.th32ProcessID == dw_process_id:
            return process.szExeFile[:-4]
    return False


def process_from_name(process_name):
    """
    From list return a process (PROCESSENTRY32) from it's name
    This function strip the .exe extention from szExeFile.

    __usage__	chrome = process_from_name("chrome")
                print 'chrome pid %s' % chrome[0].th32ProcessID
    """

    processes = []
    for process in process_list():
        if process_name == process.szExeFile[:-4]:
            processes.append(process)
    if len(processes) > 0:
        return processes
    return None
