import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

DEFAULT_DATASET_NAME = 'default_dataset'

def dataset_key(dataset_name = DEFAULT_DATASET_NAME):
    return ndb.Key('Dataset', dataset_name)

class Peoples(ndb.Model):
    first_name = ndb.StringProperty(indexed = True)
    last_name = ndb.StringProperty(indexed = True)
    phone = ndb.StringProperty(indexed = False)

class MainPage(webapp2.RequestHandler):
    def get(self):
        dataset_name = self.request.get('dataset_name',
                                        DEFAULT_DATASET_NAME)
        people_query = Peoples.query(ancestor=dataset_key(dataset_name))
        people = people_query.fetch(10)

        template_values = {
            'people': people,
            'dataset_name': urllib.quote_plus(dataset_name),
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class SearchA(webapp2.RequestHandler):
    def get(self):
        dataset_name = self.request.get('dataset_name',
                                        DEFAULT_DATASET_NAME)
        first_name = self.request.get('first_name','')
        print first_name
        people_query = Peoples.query(Peoples.first_name==first_name,
                                     ancestor=dataset_key(dataset_name))
        people = people_query.fetch(10)

        template_values = {
            'people': people,
            'dataset_name': urllib.quote_plus(dataset_name),
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class People(webapp2.RequestHandler):

    def post(self):

        dataset_name = self.request.get('dataset_name',
                                        DEFAULT_DATASET_NAME)
        people_id = self.request.get('id')
        people = Peoples(parent=dataset_key(dataset_name), id=people_id)
        
        people.first_name = self.request.get('first_name')
        people.last_name = self.request.get('last_name')
        people.phone = self.request.get('phone')
        people.put()

        query_params = {'dataset_name': dataset_name}
        self.redirect('/?'+urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', People),
    ('/SearchA', SearchA)
], debug=True)
