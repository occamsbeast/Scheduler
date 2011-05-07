"""Behaviours to assign clones
Clones objects
"""
import datetime
import calendar

from zope.interface import implements, alsoProvides
from zope.component import adapts, queryUtility
from zope.formlib import form as zform
from zExceptions import BadRequest

from collective.dexterity.appointments import MessageFactory as _
from collective.dexterity.more_widgets.widgets import YesNoFieldWidget

from plone.i18n.normalizer.interfaces import IURLNormalizer
from plone.directives import form

from plone.dexterity.utils import addContentToContainer
from plone.dexterity.utils import createContent
from plone.dexterity.utils import createContentInContainer

from rwproperty import getproperty, setproperty

from collective.dexterity.appointments.interfaces import IClone, ICloneDay, ITimeSlot, IAppointmentDay
   
alsoProvides(IClone, form.IFormFieldProvider)
alsoProvides(ICloneDay,form.IFormFieldProvider)

class CloneDay(object):
    """
    The same functionality as Clone, but adds a field for whether we want to include weekends
    """
    implements(ICloneDay)

    def __init__(self, context):
        self.context = context

    @getproperty
    def include_weekends(self):
        return 0

    @setproperty
    def include_weekends(self, value):
        #Call the clone time slot
         self.context.include_weekends = value 
 
    @getproperty
    def num_to_create(self):
        return 0

    @setproperty
    def num_to_create(self, value):
        #Call the clone time slot
        self.num_created = int(value)
        self.actionClone()
    
    def actionClone(self):
        self.parent = self.context.__parent__
        self.success = True
        self.errors = []

        if IAppointmentDay.providedBy(self.context):
            self.cloneDay() 

        else:
            self.success = False 
            self.errors.append('This is not a cloneable type')
        return 1

    def cloneDay(self):
        orig_date = self.context.appointment_date
        content = self.context.manage_copyObjects(self.context.objectIds())
        one_day = datetime.timedelta(days=1)
        self.incl_weekend = self.context.include_weekends

        i = 1
        while i < self.num_created:
            new_date = orig_date + (one_day * i)

            if self.incl_weekend or (new_date.weekday() < 5):
                try:
                    new_day = self.createNewDay(new_date,content)
                except BadRequest:
                    self.success = False
                    self.errors.append("Operation failed because there is already an object named: %s" % new_date)
            i += 1        

    def createNewDay(self, new_date,content):
        id = new_date.strftime('%a-%b.-%d-%Y')
        id = queryUtility(IURLNormalizer).normalize(id)
        #Need to copy in all of the conects of the original day

        nday = createContent('collective.dexterity.appointments.appointmentday', appointment_date=new_date)
        new_day = addContentToContainer(self.parent,nday)

        new_day.manage_pasteObjects(content)

        #Yes I know this is gross, but under time restrictions. 
        for time_slot in new_day.contentItems():
            time_slot[1].start = time_slot[1].start + (new_day.appointment_date - time_slot[1].start.date())
            time_slot[1].end = time_slot[1].end + (new_day.appointment_date - time_slot[1].end.date())

        new_day.reindexObject()     

        import pdb
        pdb.set_trace()

        return new_day


class Clone(object):
    """
    Behavior that makes copies of a given object. Useful for scheduling
    """
    implements(IClone)

    def __init__(self, context):
        self.context = context

    @getproperty
    def num_to_create(self):
        return 0

    @setproperty
    def num_to_create(self, value):
        #Call the clone time slot this needs to be changed to when the user submits the form in general
        self.num_to_clone = int(value)
        self.actionClone()
    
    def actionClone(self):
        self.parent = self.context.__parent__
        self.success = True
        self.errors = []

        if ITimeSlot.providedBy(self.context):
            self.cloneTimeSlot()            

        else:
            self.success = False 
            self.errors.append('This is not a cloneable type')
        
        return

    def cloneTimeSlot(self):
        #We need to see how we get context, and what we can do with it
        orig_start_time = self.context.start
        orig_end_time = self.context.end
        name = self.context.name
        slot_length = (orig_end_time - orig_start_time)
        max_capacity = self.context.max_capacity
        allow_waiting = self.context.allow_waitlist
        
        num_cloned = 0

        while num_cloned < self.num_to_clone:
            new_start_time = orig_start_time + (slot_length * (num_cloned + 1))
            new_end_time = orig_end_time + (slot_length *  (num_cloned + 1))
            new_time_slot = self.createNewTimeSlot(new_start_time, new_end_time, max_capacity, allow_waiting, name)
            num_cloned += 1


    def createNewTimeSlot(self, start, end, max_capacity, allow_waiting, name):
        id = (start.strftime('%I-%M-%p') + '_' + end.strftime('%I-%M-%p')).lower()

        try:
            time_slot = createContent('collective.dexterity.appointments.timeslot', start=start, end=end, name=name,
                                      max_capacity=max_capacity, allow_waitlist=allow_waiting)

            addContentToContainer(self.parent,time_slot)
        
        except BadRequest:
            self.success = False
            self.errors.append("An object already exists with id: %s" % id)
            return None
            
        new_time_slot = "lol"
        return new_time_slot
