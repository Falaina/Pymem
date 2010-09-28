"""
Process Module, module
"""

from pymem.constants.defines import MODULE_32_FIRST
from pymem.constants.defines import MODULE_32_NEXT
from pymem.constants.defines import CREATETOOLHELP_32_SNAPSHOT
from pymem.constants.defines import CLOSE_HANDLE
from pymem.constants.structures import TH32CS_CLASS
from pymem.constants.structures import MODULEENTRY32

from ctypes import sizeof
from ctypes import byref
import copy


class Module(object):
    """This Class provides the required functionalities to get process module
informations
    """

    def __init__(self, process32=None):
        """
        Module constructor, you have to provide a process32 handle.
        """

        self._process32 = process32
        self.is_process_set = self._process32 is not None

    def set_process32(self, process32):
        """
        Change or set current opened process 32
        """

        if process32 is not None:
            self._process32 = process32
            self.is_process_set = True

    def list_module32(self):
        """
        This function return a list <MODULEENTRY32> containing all available
        module for given process.
        """

        module_list = []
        if self.is_process_set:
            h_module_snap = CREATETOOLHELP_32_SNAPSHOT(\
            TH32CS_CLASS.SNAPMODULE, self._process32.th32ProcessID)
            if h_module_snap is not None:
                module_entry = MODULEENTRY32()
                module_entry.dwSize = sizeof(module_entry)
                success = MODULE_32_FIRST(h_module_snap, byref(module_entry))
                while success:
                    if module_entry.th32ProcessID == \
                    self._process32.th32ProcessID:
                        module_list.append(copy.copy(module_entry))
                    success = MODULE_32_NEXT(h_module_snap, \
                    byref(module_entry))
                CLOSE_HANDLE(h_module_snap)
        return module_list

    def has_module32(self, module):
        """
        Return True if current process has loaded given module (dll)
        """

        if module[-4:] != '.dll':
            module += '.dll'
        module_list = self.list_module32()
        for m in module_list:
            if module in m.szExePath.split("\\"):
                return True
        return False
