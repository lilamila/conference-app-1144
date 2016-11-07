#!/usr/bin/env python

"""models.py

Conference server-side Python App Engine data & ProtoRPC models

$Id: models.py,v 1.1 2014/05/24 22:01:10 mleafer Exp $

created/forked from conferences.py by mleafer on 2016 may 22

"""

__author__ = 'mariesleaf@gmail.com (Marie Leaf)'

import httplib
import endpoints
from protorpc import messages
from google.appengine.ext import ndb

class ConflictException(endpoints.ServiceException):
    """ConflictException -- exception mapped to HTTP 409 response"""
    http_status = httplib.CONFLICT

# Models ---------
# needs to come before Profile class because of Session to add to wishlist
class Session(ndb.Model):
    """Session -- Session object"""
    sessionName     = ndb.StringProperty(required=True)
    highlights      = ndb.StringProperty(repeated=True)
    speaker         = ndb.StringProperty(required=True)
    duration        = ndb.IntegerProperty()
    typeOfSession   = ndb.StringProperty() # use enum?
    date            = ndb.DateProperty()
    startTime       = ndb.TimeProperty() # in 24 hr notation so it can be ordered
    organizerUserId = ndb.StringProperty()
    websafeConferenceKey  = ndb.StringProperty()

# defines input parameters for _createSessionObject
class SessionForm(messages.Message):
    """SessionForm -- Session outbound form message"""
    sessionName          = messages.StringField(1)
    highlights           = messages.StringField(2, repeated=True)
    speaker              = messages.StringField(3)
    duration             = messages.IntegerField(4, variant=messages.Variant.INT32)
    typeOfSession        = messages.StringField(5) # use enum?
    date                 = messages.StringField(6) # DateField()
    startTime            = messages.StringField(7) # TimeField()
    organizerUserId = messages.StringField(8)
    websafeSessionKey = messages.StringField(9)
    websafeConferenceKey  = messages.StringField(10)

class SessionForms(messages.Message):
    """SessionForms -- multiple Session outbound form message"""
    items = messages.MessageField(SessionForm, 1, repeated=True)


class SessionQueryForm(messages.Message):
    """SessionQueryForm -- Session query inbound form message"""
    field = messages.StringField(1)
    operator = messages.StringField(2)
    value = messages.StringField(3)

class SessionQueryForms(messages.Message):
    """ConferenceQueryForms -- multiple SessionQueryForm inbound form message"""
    filters = messages.MessageField(SessionQueryForm, 1, repeated=True)

class Profile(ndb.Model):
    """Profile -- User profile object"""
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    teeShirtSize = ndb.StringProperty(default='NOT_SPECIFIED')
    conferenceKeysToAttend = ndb.StringProperty(repeated=True)
    sessKeyWishlist = ndb.KeyProperty(Session, repeated=True)

# only editable by users
class ProfileMiniForm(messages.Message):
    """ProfileMiniForm -- update Profile form message"""
    displayName = messages.StringField(1)
    teeShirtSize = messages.EnumField('TeeShirtSize', 2)

class ProfileForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    teeShirtSize = messages.EnumField('TeeShirtSize', 3)
    conferenceKeysToAttend = messages.StringField(4, repeated=True)

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)

class BooleanMessage(messages.Message):
    """BooleanMessage-- outbound Boolean value message"""
    data = messages.BooleanField(1)

class Conference(ndb.Model):
    """Conference -- Conference object"""
    name            = ndb.StringProperty(required=True)
    description     = ndb.StringProperty()
    organizerUserId = ndb.StringProperty()
    topics          = ndb.StringProperty(repeated=True)
    city            = ndb.StringProperty()
    startDate       = ndb.DateProperty()
    month           = ndb.IntegerProperty() # TODO: do we need for indexing like Java?
    endDate         = ndb.DateProperty()
    maxAttendees    = ndb.IntegerProperty()
    seatsAvailable  = ndb.IntegerProperty()

    @property
    def sessions(self):
        return Session.query(ancestor=self.key)

class ConferenceForm(messages.Message):
    """ConferenceForm -- Conference outbound form message"""
    name            = messages.StringField(1)
    description     = messages.StringField(2)
    organizerUserId = messages.StringField(3)
    topics          = messages.StringField(4, repeated=True)
    city            = messages.StringField(5)
    startDate       = messages.StringField(6) #DateTimeField()
    month           = messages.IntegerField(7, variant=messages.Variant.INT32)
    maxAttendees    = messages.IntegerField(8, variant=messages.Variant.INT32)
    seatsAvailable  = messages.IntegerField(9, variant=messages.Variant.INT32)
    endDate         = messages.StringField(10) #DateTimeField()
    websafeConferenceKey = messages.StringField(11)
    organizerDisplayName = messages.StringField(12)

class ConferenceForms(messages.Message):
    """ConferenceForms -- multiple Conference outbound form message"""
    items = messages.MessageField(ConferenceForm, 1, repeated=True)

class TeeShirtSize(messages.Enum):
    """TeeShirtSize -- t-shirt size enumeration value"""
    NOT_SPECIFIED = 1
    XS_M = 2
    XS_W = 3
    S_M = 4
    S_W = 5
    M_M = 6
    M_W = 7
    L_M = 8
    L_W = 9
    XL_M = 10
    XL_W = 11
    XXL_M = 12
    XXL_W = 13
    XXXL_M = 14
    XXXL_W = 15

class ConferenceQueryForm(messages.Message):
    """ConferenceQueryForm -- Conference query inbound form message"""
    field = messages.StringField(1)
    operator = messages.StringField(2)
    value = messages.StringField(3)

class ConferenceQueryForms(messages.Message):
    """ConferenceQueryForms -- multiple ConferenceQueryForm inbound form message"""
    filters = messages.MessageField(ConferenceQueryForm, 1, repeated=True)

class SocialForm(messages.Message):
    """ProfileFeedForm -- Social Feed inbound/outbound form message"""
    displayName = messages.StringField(1)
    conferenceKeysToAttend = messages.StringField(2, repeated=True)
    websafeConferenceKey = messages.StringField(3)

class SocialForms(messages.Message):
    """ConferenceForms -- multiple Conference outbound form message"""
    socialList = messages.MessageField(SocialForm, 1, repeated=True)

class Speaker(ndb.Model):
    """Speaker -- Speaker profile object"""
    displayName = ndb.StringProperty(required=True)
    mainEmail = ndb.StringProperty(required=True)
    bio = ndb.TextProperty()
    # sessionKeys = ndb.KeyProperty(Session, repeated=True)
    sessionKeys = ndb.StringProperty(repeated=True)

class SpeakerForm(messages.Message):
    """SpeakerForm -- Speaker outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    bio = messages.StringField(3)
    sessionKeys = messages.StringField(4, repeated=True)

class SpeakerMiniForm(messages.Message):
    """SpeakerMiniForm -- Speaker outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)

class SpeakerList(messages.Message):
    items = messages.MessageField(SpeakerMiniForm, 1, repeated=True)