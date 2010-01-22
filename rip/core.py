from urlparse import urljoin, urlparse

from docutils.core import publish_parts
from docutils.writers.html4css1 import HTMLTranslator, Writer

DEFAULT_FACTORIES = ('rip.workers.code', 'rip.workers.latex')

class RIPException(Exception) :
    pass

class ReSTinPeaceHTMLTranlsator(HTMLTranslator) :

    controller = None

    def __init__(self, document) :
        HTMLTranslator.__init__(self, document)

    def visit_image(self, node) :
        if not urlparse(node['uri']).scheme :
            # Don't insert prefix if URL is absolute.
            node['uri'] = urljoin(self.controller.state['image_uri_prefix'], node['uri'])

        return HTMLTranslator.visit_image(self, node)

class ReSTinPeaceHTMLWriter(Writer) :
    def __init__(self) :
        Writer.__init__(self)
        self.translator_class = ReSTinPeaceHTMLTranlsator

class Controller(object) :
    '''Controls the ReStuctured Text -> HTML transformation process.'''

    defaults = {
        'doctitle_xform' : False,
        'footnote_references' : 'superscript',
        'initial_header_level' : 1,
        'report_level' : 3,
        'tab_width' : 4,
        'image_uri_prefix' : '',
    }

    def __init__(self, factories = DEFAULT_FACTORIES, **overrides) :
        self.settings = {}
        self.settings.update(Controller.defaults)

        for factory in factories :
            try :
                interface = __import__(factory, fromlist = ['interface']).interface
            except RIPException :
                continue

            for worker_name in interface.EXPORTS :
                worker = getattr(interface, worker_name)
                worker.controller = self
                self.settings.update(worker.defaults)

        self.settings.update(overrides)

    def render(self, text, **overrides) :
        '''Renders ReStructured Text into HTML.'''

        self.state = {}
        self.state.update(self.settings)
        self.state.update(overrides)

        ReSTinPeaceHTMLTranlsator.controller = self

        return publish_parts(
            text,
            writer = ReSTinPeaceHTMLWriter(),
            settings_overrides = self.state,
        )['fragment']

markup = Controller()
