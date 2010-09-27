"""
Pymem global contribution functions and decorators.
"""


def is_init(module):
    def _is_init(function):
        def decorated(self, *args, **kwargs):
            if getattr(self, module) is None:
                getattr(self, '_init_%s' % module)()
            return function(self, *args)
        return decorated
    return _is_init
