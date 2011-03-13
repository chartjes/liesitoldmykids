"""
views.py

URL routes and handlers

"""
import uuid

from google.appengine.api import taskqueue
from google.appengine.api import users

from flask import render_template, flash, url_for, redirect
from he3.db.tower.paging import PageLinks, PagedQuery

from forms import LieForm
from models import LieModel

from defensio import *

def main(current_page=1):
    query = LieModel.all().filter('status = ', 'approved')

    """Add some logic later to figure out if we have a new page"""
    pagedQuery = PagedQuery(query, 10)
    pagedQuery.order('-timestamp')
    lies = pagedQuery.fetch_page(current_page)
    page_count = pagedQuery.page_count() 

    lieLinks = PageLinks(page = current_page, page_count = pagedQuery.page_count(), url_root = "/", page_field = 'page', page_range = 5)
    navigation_links = lieLinks.get_links()

    return render_template('list_lies.html', lies=lies, navigation_links = navigation_links)

def new_lie():
    form = LieForm()

    if form.validate_on_submit():
        lie_key_name = str(uuid.uuid1())
        new_lie = LieModel(
                key_name = lie_key_name,
                title = form.title.data,
                body = form.body.data,
                status = 'pending'
                )
        new_lie.put()
        flash(u'Thanks for submitting a new lie!')
        taskqueue.add(url='/tasks/check_for_spam', params={'lie_key': lie_key_name})
        return redirect(url_for('main'))

    return render_template('new_lie.html', form=form) 

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

