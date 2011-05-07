from zope import schema
from zope.interface import Interface
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from zExceptions import BadRequest

from DateTime import DateTime

from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IURLNormalizer


def _getContext(self):
    self = self.aq_parent
    while getattr(self, '_is_wrapperish', None):
        self = self.aq_parent
    return self    
            
ZopeTwoPageTemplateFile._getContext = _getContext

# End ugly hack.

class IClone(Interface):
    numToCreate = schema.Int(title=u'Number to Create', description=u'The number of clones to create', required=True)

class ICloneDay(IClone):
    includeWeekends = schema.Bool(title=u'Include Weekends', description=u'Do you want to include weekends?')

class ICloneTimeSlot(IClone):
    pass

class CloneForm(formbase.PageForm):
    result_template = ZopeTwoPageTemplateFile('cloning-results.pt')
    success = True
    errors = []
    form_fields = form.FormFields(IClone)
    
    def __init__(self, context, request):
        formbase.PageForm.__init__(self, context, request)

        if IDay.providedBy(context):
            self.form_fields = form.FormFields(ICloneDay)
        elif ITimeSlot.providedBy(context):
            self.form_fields = form.FormFields(ICloneTimeSlot)
        else:
            self.form_fields = form.FormFields(IClone)
            
    @form.action('Clone')
    def action_clone(self, action, data):
        self.parent = self.context.aq_inner.aq_parent 
        self.success = True
        self.errors = []
        self.numToCreate = data['numToCreate']
        if 'includeWeekends' in data:
            self.includeWeekends = data['includeWeekends']
        
        if IDay.providedBy(self.context):
            self.cloneDay()            
        elif ITimeSlot.providedBy(self.context):
            self.cloneTimeSlot()            
        else:
            self.success = False 
            self.errors.append('This is not a cloneable type')
        
        return self.result_template()
   
    def cloneDay(self):
        origDate = self.context.getDate()
        contents = self.context.manage_copyObjects(self.context.objectIds())
        numCreated = 0
        
        i = 1
        while numCreated < self.numToCreate:
            newDate = origDate + i
            if self.includeWeekends or (newDate.aDay() not in ['Sat', 'Sun']):
                try:
                    newDay = self.createNewDay(newDate, contents)
                except BadRequest:
                    self.success = False
                    self.errors.append("Operation failed because there is already an object named: %s" % newDate)
                else:
                    numCreated += 1
                    if numCreated == 1:
                        newDay.removeAllPeople()
                        contents = newDay.manage_copyObjects(newDay.objectIds())
            i += 1        
                
    def createNewDay(self, date, contents):
        id = date.strftime('%a-%b.-%d-%Y')
        id = queryUtility(IURLNormalizer).normalize(id)
        self.parent.invokeFactory('Day', id, date=date)            
        newDay = self.parent[id]
        newDay.manage_pasteObjects(contents)
        newDay.reindexObject()     
        return newDay
        
    def cloneTimeSlot(self):
        origStartTime = self.context.getStartTime()
        origEndTime = self.context.getEndTime()
        name = self.context.getName()
        slotLength = (float(origEndTime) - float(origStartTime)) / 60 / 60 / 24
        maxCapacity = self.context.getMaxCapacity()
        allowWaiting = self.context.getAllowWaitingList()
        
        numCreated = 0
        while numCreated < self.numToCreate:
            newStartTime = origStartTime + (slotLength * (numCreated + 1))
            newEndTime = origEndTime + (slotLength *  (numCreated + 1))
            newTimeSlot = self.createNewTimeSlot(newStartTime, newEndTime, maxCapacity, allowWaiting, name)
            numCreated += 1

    def createNewTimeSlot(self, startTime, endTime, maxCapacity, allowWaiting, name):
        id = (startTime.strftime('%I-%M-%p') + '-' + endTime.strftime('%I-%M-%p')).lower()
        if name != '':
            id = name + '-' + id
        id = queryUtility(IURLNormalizer).normalize(id)

        try:
            self.parent.invokeFactory('Time Slot', id, startTime=startTime, endTime=endTime, name=name,
                                      maxCapacity=maxCapacity, allowWaitingList=allowWaiting)
        except BadRequest:
            self.success = False
            self.errors.append("An object already exists with id: %s" % id)
            return None
            
        newTimeSlot = self.parent[id]
        return newTimeSlot
