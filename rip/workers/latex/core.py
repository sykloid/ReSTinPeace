import os
import hashlib
import shutil
import tempfile

from docutils import nodes
from docutils.parsers.rst import directives, Directive, roles
from docutils.parsers.rst.directives.images import Image

from .templates import latex_document_template

class LaTeXDirective(Directive) :
    '''A ReStructured Text Directive to render formulae as LaTeX images.'''

    has_content = True

    defaults = {
        'latex_command' : 'latex --interaction=nonstopmode {hash}.tex',
        'latex_convert_command' : \
            'convert -density 120 -trim -transparent "#FFFFFF" {hash}.ps {hash}.{extension}',
        'latex_document_template' : latex_document_template,
        'latex_dvips_command' : 'dvips -E {hash}.dvi -o {hash}.ps',
        'latex_font_size' : 11,
        'latex_image_directory' : os.getcwd(),
        'latex_image_extension' : 'png',
        'latex_image_uri' : './{image_file}',
    }
    controller = None

    def render_latex_as_image(self, formula) :
        '''Render the given formula as an image, and return its file name.'''

        # The name of the created image will be the hash of the formula, with
        # the specified image extension
        formula_hash = hashlib.md5(formula).hexdigest()
        file_name = formula_hash + '.' + self.controller.state['latex_image_extension']
        file_path = os.path.join(
            self.controller.state['latex_image_directory'],
            file_name,
        )

        # Look for an image with the same hash, return it if it exists.
        if os.path.exists(file_path) :
            return file_name

        tmpdir = tempfile.mkdtemp()
        current_path = os.getcwd()
        os.chdir(tmpdir)

        # Write the latex template to a temporary file, and interpolate with
        # formula and font size.
        open(formula_hash + '.tex', 'w').write(
            self.controller.state['latex_document_template'].format(
                font_size = self.controller.state['latex_font_size'],
                formula = formula,
            )
        )

        # 1. LaTeX -> DVI   with latex.
        # 2. DVI   -> PS    with dvips.
        # 3. PS    -> Image with convert.
        os.system(self.controller.state['latex_command'].format(hash = formula_hash))
        os.system(self.controller.state['latex_dvips_command'].format(hash = formula_hash))
        os.system(self.controller.state['latex_convert_command'].format(
            hash = formula_hash,
            extension = self.controller.state['latex_image_extension'],
        ))

        # Copy the rendered image to the destination directory.
        shutil.copyfile(
            os.path.join(
                tmpdir,
                formula_hash + '.' + self.controller.state['latex_image_extension'],
            ),
            file_path
        )

        # Clean Up.
        os.chdir(current_path)
        shutil.rmtree(tmpdir)

        return file_name

    def run(self) :
        formula = '\n'.join(self.content)
        image = self.render_latex_as_image(formula)
        uri = self.controller.state['latex_image_uri'].format(image_file = image)

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

def LaTeXRole(name, raw, text, line, inliner, options = {}, content = []) :
    formula = text.replace('\\\\', '\\')
    uri = render_latex_as_image(formula)

    return (Image(
        name = name,
        arguments = [uri],
        options = {'classes' : ['latex', 'latex-inline']},
        content = None,
        lineno = line,
        content_offset = None,
        block_text = None,
        state = None,
        state_machine = None,
    ).run(), [])

LaTeXRole.defaults = {}
