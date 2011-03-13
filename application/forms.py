"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators


class ExampleForm(wtf.Form):
    example_id = wtf.TextField('Example ID', validators=[validators.Required()])
    example_title = wtf.TextField('Example Title', validators=[validators.Required()])

class LieForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required()])
    body = wtf.TextAreaField('What did you lie about?', validators=[validators.Required()])

