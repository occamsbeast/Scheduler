from collective.dexterity.appointments import MessageFactory as _

from collective.dexterity.appointments.interfaces import IAppointmentDay
from plone.app.content.interfaces import INameFromTitle

from five import grok

from zope import interface
from plone.dexterity import content


class AppointmentDay(content.Container):
    """
    A Sign up sheet for appointments
    """
    
    interface.implements(IAppointmentDay)
    

# class AppointmentDayNameGenerator(grok.Adapter):
#     """
#     Foo is Bar
#     """
#     foo = 'bar'
    
class AppointmentDayNameGenerator(grok.Adapter):
    """
    Generates the id for a day that matches the date of the appointment day
    """
    grok.context(IAppointmentDay)
    grok.provides(INameFromTitle)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def title(self):
        return unicode(self.context.appointment_date.isoformat())