from collective.dexterity.appointments import MessageFactory as _

from collective.dexterity.appointments.interfaces import ITimeSlot
from zope import interface
from plone.dexterity import content
from five import grok
from plone.app.content.interfaces import INameFromTitle
from DateTime import DateTime
from zope.schema.fieldproperty import FieldProperty
from rwproperty import getproperty, setproperty


class TimeSlot(content.Container):
    """
    A Sign up sheet for appointments
    """
    
    interface.implements(ITimeSlot)
    start = FieldProperty(ITimeSlot["start"])

    @property
    def full(self):
        """
            Return whether the object is full or not
        """
        if len(self.objectIds()) >= self.max_capacity:
            fullest = True
        else:
            fullest = False

        self.reindexObject()
        return fullest

    @property
    def date_str(self):
        """
            Return whether the object is full or not
        """
        return self.start.strftime("%b %d %Y")

    @property
    def start_str(self):
        """
            Return whether the object is full or not
        """
        return self.start.strftime("%I:%M %p") 

    @property
    def end_str(self):
        """
            Return whether the object is full or not
        """
        return self.end.strftime("%I:%M %p") 


class TimeSlotNameGenerator(grok.Adapter):
    """
    Generates the id for a day that matches the date of the appointment day
    """
    grok.context(ITimeSlot)
    grok.provides(INameFromTitle)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def title(self):
        return unicode(self.context.start.time().isoformat())
