from docutils.core import publish_parts
from docutils.writers.html4css1 import Writer

DEFAULT_FACTORIES = ()

class RIPException(Exception) :
    pass

class Controller(object) :
    '''Controls the ReStuctured Text -> HTML transformation process.'''

    defaults = {
        'doctitle_xform' : False,
        'footnote_references' : 'superscript',
        'initial_header_level' : 1,
        'report_level' = 3,
        'tab_width' : 4,
    }

    def __init__(self, factories = DEFAULT_FACTORIES, **overrides) :
        self.settings = {}
        self.settings.update(Controller.defaults)
        self.settings.update(overrides)

        for factory in factories :
            try :
                interface = __import__(factory, fromlist = ['interface']).interface
            except RIPException :
                continue

            for worker_name in interface.EXPORTS :
                worker = getattr(interface, worker_name)
                worker.controller = self
                self.settings.update(worker.defaults)

    def render(self, text, **overrides) :
        '''Renders ReStructured Text into HTML.'''

        self.state = {}
        self.state.update(self.settings)
        self.state.update(overrides)

        return publish_parts(
            text,
            writer = Writer(),
            settings_overrides = self.state,
        )['fragment']

markup = Controller()
