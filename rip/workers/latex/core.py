import os
import hashlib
import shutil
import tempfile

from docutils import nodes
from docutils.parsers.rst import directives, Directive, roles
from docutils.parsers.rst.directives.images import Image

class LaTeXDirective(Directive) :
    '''A ReStructured Text Directive to render formulae as LaTeX images.'''

    has_content = True

    defaults = {
        'latex_image_uri' : './{image_file}',
    }
    controller = None

    def render_latex_as_image(formula

    def run(self) :
        formula = '\n'.join(self.content)
        image = render_latex_as_image(formula)
        uri = self.controller['latex_image_uri'].format(image_file = image)

        return Image(
            name = self.name,
            arguments = [uri],
            options = {'align' : 'center', 'classes' : ['latex',]},
            content = None,
            lineno = self.lineno,
            content_offset = self.content_offset,
            block_text = self.block_text,
            state = self.state,
            state_machine = self.state_machine,
        ).run()
