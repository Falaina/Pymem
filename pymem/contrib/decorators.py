"""
Pymem global contribution functions and decorators.
"""


def is_init(module):
    """
    Initialize a module is this one is None
    """

    def _is_init(function):
        """
        Level 1 wrapper
        """

        def decorated(self, *args):
            """
            Level 2 wrapper
            """

            if getattr(self, module) is None:
                getattr(self, '_init_%s' % module)()
            return function(self, *args)
        return decorated
    return _is_init


def has_handle():
    """
    Assert h_process is opened.
    """

    def _has_handle(function):
        """
        Level 1 wrapper
        """

        def decorated(self, *args):
            """
            Level 2 wrapper
            """

            className = self.__class__.__name__
            if hasattr(self, '_h_process'):
                if getattr(self, '_h_process') is not None:
                    ret = function(self, *args)
                    return ret
                else:
                    raise Exception("In object %s attribute h_process is \
                    None when calling method: %s" % \
                    (className, function.__name__))
            else:
                raise Exception("%s has not attribute: %s" % \
                (className, 'h_process'))
        return decorated
    return _has_handle
