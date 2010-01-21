from docutils.parsers.rst import directives, Directive

from operator import not_

class CodeDirective(Directive) :
    '''A ReStructured Text Directive to highlight code blocks using pygments.'''

    require_arguments = 0
    optional_arguments = 1
    option_spec = {
        'linenos' : not_,
        'style' : directives.unchanged,
        'noclasses' : not_,
    }

    has_content = True

def CodeRole() :
    pass
