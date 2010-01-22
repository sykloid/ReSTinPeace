import os

from rip.core import RIPException

def binary_exists(binary) :
    '''Checks if a given binary exists, and is executable.'''

    path, name = os.path.split(binary)

    if path :
        return os.path.exists(binary) and os.access(binary, os.X_OK)

    executables = (
        os.path.join(path, name)
        for path in os.environ["PATH"].split(os.pathsep)
    )

    return any(
        os.path.exists(file) and os.access(file, os.X_OK)
        for file in executables
    )

binaries = ('latex', 'dvips', 'convert')

for binary in binaries :
    if not binary_exists(binary) :
        raise RIPException

from .core import LaTeXDirective, LaTeXRole
from docutils.parsers.rst.directives import register_directive
from docutils.parsers.rst.roles import register_canonical_role

register_directive('latex', LaTeXDirective)
register_canonical_role('latex', LaTeXRole)

EXPORTS = ('LaTeXDirective', 'LaTeXRole')
