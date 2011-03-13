"""
models.py

App Engine datastore models

"""

from google.appengine.ext import db

class ExampleModel(db.Model):
    """Example Model"""
    example_id = db.StringProperty(required=True)
    example_title = db.StringProperty(required=True)
    added_by = db.UserProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)

class LieModel(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True)

