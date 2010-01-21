from rip.core import RIPException

try :
    import pygments
    import docutils
except ImportError :
    raise RIPError

from .core import CodeDirective, CodeRole

from docutils.parsers.rst.directives import register_directive

register_directive('code', CodeDirective)

EXPORTS = ('CodeDirective', 'CodeRole')
