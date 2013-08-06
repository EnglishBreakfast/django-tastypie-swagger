from urlparse import urljoin

from django.conf import settings

from markdown import Markdown
from lxml import etree

def trailing_slash_or_none():
    """
    Return a slash or empty string based on tastypie setting
    """
    if getattr(settings, 'TASTYPIE_ALLOW_MISSING_SLASH', False):
        return ''
    return '/'


def urljoin_forced(base, path, **kwargs):
    """
    urljoin base with path, except append '/' to base if it doesnt exist
    """
    base = base.endswith('/') and base or '%s/' % base
    return urljoin(base, path, **kwargs)

def md_parse_docs(fn):
    """
    Parse a markdown document into (section, field) keyed dict of
    docstrings.
    """

    md = Markdown(safe_mode='escape')
    with open(fn, 'r') as f_in:
        docs_html = md.convert(f_in.read())
        etr = etree.HTML(docs_html)

    docs = {}
    section = ''
    field = ''
    first_h1 = etr.find('body/h1')

    if first_h1 is not None:
        section, field = first_h1.text, ''
        for e in first_h1.itersiblings():
            if e.tag == 'h1':
                section, field = e.text, ''
            elif e.tag == 'h2':
                field = e.text
            else:
                docs[(section, field)] = docs.get((section, field), '') + etree.tostring(e)
    return docs
