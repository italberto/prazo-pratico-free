import os
import webapp2
import jinja2
#funcoes de login
import sigaa

#settings for configurate the render templates html
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        #try to get the session cookie
        cookie_value = self.request.cookies.get("user")
        #if cookie exists
        if cookie_value:
            t = jinja_env.get_template('index.html')
        else:
            t = jinja_env.get_template('login.html')
        self.response.out.write(t.render( error = ""))

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        #if the data is full correctly
        if username and password:
            pass



app = webapp2.WSGIApplication([('/', MainPage)])
