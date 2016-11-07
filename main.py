#!/usr/bin/env python

"""
main.py -- Conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by mleafer on 2016 may 22

"""

__author__ = 'mariesleaf@gmail.com (Marie Leaf)'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from conference import ConferenceApi
import logging
logging.getLogger().setLevel(logging.DEBUG)


MEMCACHE_FEATURED_SPEAKER = "FEATURED SPEAKER"
FEATURED_SPEAKER_TPL = ('Featured Speaker %s is presenting %s')

class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )

# https://github.com/apeabody/P4/blob/master/main.py
class SetFeaturedSpeakerHandler(webapp2.RequestHandler):
    print '****MARKER FOR setfeaturedspeakerhandler TASKQUE CALL'
    def post(self):
        """Check and Set Featured Speaker """
        C_API = ConferenceApi()
        featured_speaker = self.request.get('speaker')

        logging.debug(featured_speaker)
        print featured_speaker

        websafeConferenceKey = self.request.get('websafeConferenceKey')

        C_API._setFeaturedSpeaker(featured_speaker, websafeConferenceKey)


app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/set_featured_speaker', SetFeaturedSpeakerHandler)
], debug=True)
