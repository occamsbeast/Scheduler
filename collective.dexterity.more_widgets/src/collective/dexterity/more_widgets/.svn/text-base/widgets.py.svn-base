""" Custom wigets and overrides. """


from z3c.form import term
from z3c.form.browser.radio import RadioFieldWidget

from z3c.form.browser import widget

from five import grok

def YesNoFieldWidget(field, request):
    """Used by z3c.form"""

    class BoolTerms(term.BoolTerms):
        trueLabel = u"Yes"
        falseLabel = u"No"

    widget=RadioFieldWidget(field, request)
    widget.terms=BoolTerms(None, None, None, field, None)
    return widget
