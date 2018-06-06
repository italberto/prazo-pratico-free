import os
import webapp2
import jinja2
import json
import base64
#funcoes de login
import sigaa

#settings for configurate the render templates html
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class MainPage(webapp2.RequestHandler):
    """index page"""
    def get(self):
        t = jinja_env.get_template('index.html')
        self.response.out.write(t.render())



class LoginPage(webapp2.RequestHandler):
    """Login page"""
    def get(self, error="", user=""):
        t = jinja_env.get_template('login.html')
        self.response.out.write(t.render(error=error, username=user))

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        #if the data is full correctly
        if username and password:
            #make login
            login = sigaa.login(username, password)
            #if user or password is wrong
            if login:
                login_json = json.dumps(login)
                self.response.headers['Set-Cookie'] = 'user='+base64.b64encode(login_json)
                self.redirect('/home')

            else:
                self.get("Senha ou usuario invalidos.", username)
                pass

class Home(webapp2.RequestHandler):
    def get(self):
        cookie_value = self.request.cookies.get('user')
        cookie_value = base64.b64decode(cookie_value)
        cookie = json.loads(cookie_value)
        print cookie

        if cookie_value:

            pass





app = webapp2.WSGIApplication([('/', MainPage), ('/login', LoginPage), ('/home', Home)])
