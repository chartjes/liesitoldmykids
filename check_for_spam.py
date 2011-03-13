import logging

from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from defensio import *

logger = logging.getLogger(__name__)

class LieModel(db.Model):
    lie_id = db.StringProperty()
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True)

class SpamChecker(webapp.RequestHandler):
    def post(self):
        lie_key = self.request.get('lie_key')
        lie_k = db.Key.from_path('LieModel', lie_key)
        lie = db.get(lie_k)
        client = Defensio('DEFENSIO API KEY HERE') 
        lie_is_spam = False
        title_doc = {'content': lie.title, 'type': 'comment', 'platform':'python'}
        body_doc = {'content': lie.body, 'type': 'comment', 'platform':'python'}
        title_status,title_response = client.post_document(title_doc)
        body_status,body_response = client.post_document(body_doc)

        if title_status == 200 and title_response['defensio-result']['spaminess'] > 0.5:
            lie_is_spam = True

        if body_status == 200 and body_response['defensio-result']['spaminess'] > 0.5:
            lie_is_spam = True

        if lie_is_spam == True:
            logger.info('Submission is spam')
            db.delete(lie_k) 


def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/tasks/check_for_spam', SpamChecker),
        ]))

if __name__ == '__main__':
    main()
