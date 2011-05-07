from collective.dexterity.appointments import MessageFactory as _

from collective.dexterity.appointments import interfaces

from zope import interface
from plone.dexterity import content


class SignupSheet(content.Container):
    """
    A Sign up sheet for appointments
    """
    
    interface.implements(interfaces.ISignupSheet)