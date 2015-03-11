import os
from mako.lookup import TemplateLookup


TEMPLATE_PATH = os.path.realpath('./web')
TEMPLATE_LOOKUP = TemplateLookup(directories=[TEMPLATE_PATH])


def template(name, **kwargs):
    tpl = TEMPLATE_LOOKUP.get_template(name)
    return tpl.render(**kwargs)