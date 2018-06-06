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
        t = jinja_env.get_template('index.html')
        self.response.out.write(t.render())



class LoginPage(webapp2.RequestHandler):
    def get(self, error="", user=""):
        t = jinja_env.get_template('login.html')
        self.response.out.write(t.render(error=error, username=user))

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        #if the data is full correctly
        if username and password:
            if sigaa.login(username, password):
                self.response.out.write('OK')
            #if user or password is wrong
            else:
                self.get("Senha ou usuario invalidos.", username)
                pass





app = webapp2.WSGIApplication([('/', MainPage), ('/login', LoginPage)])
