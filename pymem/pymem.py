"""
Pymem module.
"""

from modules.process import Process
from modules.process import process_from_name
from contrib.decorators import is_init


class Pymem(object):
    """Provides class instance methods for general process and memory
manipulations.
    """

    def __init__(self):
        """
        Initialize pymem objects
        """

        self.process = None
        self.pid = None  # refractor
        self.process32 = None  # refractor
        self.process_handle = None

    def _init_process(self):
        """
        Initialize process class when it's needed by pymem.
        """

        self.process = Process()

    @is_init('process')
    def open_process(self, process_id, debug=True):
        """
        Opens a process for interaction.
        """

        if debug:
            if self.process.open_debug(process_id):
                self.process_handle = self.process.h_process
                self.pid = process_id
                self.process32 = self.process.process32
                return True
            return False
        return self.process.open(process_id)

    @is_init('process')
    def open_process_from_name(self, process_name, debug=True, number=0):
        """
        Opens a process from its name for interaction.
        """

        processes = process_from_name(process_name)
        if processes is not None:
            if len(processes) - 1 == number:
                process = processes[len(processes) - 1]
                return self.open_process(process.th32ProcessID, debug)
        return False
