import webapp2
import jinja2
import logging
import os
from search_engine_mine import return_jobs_from_dice2
from search_engine_mine import stack_jobs
from search_engine_mine import get_monster_jobs2
from search_engine_mine import get_careerbuilder_jobs
from search_engine_mine import get_indeed_jobs


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)



class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def render_json(self, d):
		json_text = json.dumps(d)
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		self.write(json_text)

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		if self.request.url.endswith('.json'):
			self.format = 'json'
		else:
			self.format = 'html'




class MainHandler(Handler):
	def get(self):
		self.render('main.html')

	def post(self):
		position = self.request.get('position')
		location = self.request.get('location')
		
		if position and location:
			jobs = []
			jobs += return_jobs_from_dice2(position, location)
			jobs += stack_jobs(position, location)
			jobs += get_monster_jobs2(position, location)
			jobs += get_careerbuilder_jobs(position, location)
			jobs += get_indeed_jobs(position, location)
			for i in jobs:
				for e in jobs:
					if e != i and e.text == i.text:
						del jobs[jobs.index(e)]	
			jobs_dict = {}
			for i in jobs:
				key = i.text.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
				jobs_dict[key] = i.absolute_url

			self.render('main.html', position = position, location = location, jobs_dict = jobs_dict)

		else:
			error = 'We need a position AND location to continue'
			logging.error('Hit an error')
			self.render('main.html', error = error)





app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
