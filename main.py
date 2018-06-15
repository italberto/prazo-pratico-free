#encoding=utf8
import os
import webapp2
import jinja2
import json
import base64
import httplib # for exception HTTPException
#funcoes de login
import sigaa

from google.appengine.ext import db

#settings for configurate the render templates html
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class User(db.Model):
    username = db.StringProperty(required=True)
    json_data = db.TextProperty(required=True)

class MainPage(webapp2.RequestHandler):
    """index page"""
    def get(self):
        count_users = db.GqlQuery("SELECT * FROM User").count()
        t = jinja_env.get_template('index.html')
        self.response.out.write(t.render(count_users=count_users))



class LoginPage(webapp2.RequestHandler):
    """Login page"""
    def get(self, error="", user=""):
        count_users = db.GqlQuery("SELECT * FROM User").count()
        t = jinja_env.get_template('login.html')
        self.response.out.write(t.render(error=error, username=user, count_users=count_users))

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        login = ''

        #if the data is full correctly
        if username and password:
            #make login
            try:
                login = sigaa.login(username, password)
            except httplib.HTTPException:
                print 'SIGAA não respondeu em tempo, timeout;'
                self.redirect('/error')
            #if user or password is wrong
            if login:
                login_json = json.dumps(login)

                #verificar se ja tem cadastro
                user_verify = db.GqlQuery("SELECT * FROM User WHERE username = \'" + username + "\'").get()
                #se ja tiver cadastro
                if user_verify:
                    user_verify.username = username
                    user_verify.json_data = login_json
                    user_verify.put()
                else:

                    user = User(username=username, json_data=login_json)

                    user.put()

                self.response.headers['Set-Cookie'] = 'user=' + username.encode("utf-8")
                self.response.out.write('Logando...')
                self.redirect('/home')

            else:
                self.get("Senha ou usuário inválidos.", username)
                pass

class Home(webapp2.RequestHandler):
    def get(self):
        username = self.request.cookies.get('user')
        #cookie_value = base64.b64decode(cookie_value)

        #if we have a valid cookie
        if username:
            user_consult = db.GqlQuery("SELECT * FROM User WHERE username = \'" + username + "\'").get()
            user = json.loads(user_consult.json_data)

            print user
            t = jinja_env.get_template('home.html')
            self.response.out.write(t.render(username=user['username'], classes= user['classes']))
        else:
            self.redirect('/login')

class LogOut(webapp2.RequestHandler):
    """To make logout of the account, and clean the document.cookie"""
    def get(self):
        self.response.headers['Set-Cookie'] = ''
        self.response.out.write('')
        self.redirect('/')

class Donations(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template('donations.html')
        self.response.out.write(t.render())

class ErrorPage(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template('error.html')
        self.response.out.write(t.render())



app = webapp2.WSGIApplication([('/', MainPage), ('/login', LoginPage), ('/home', Home), ('/logout', LogOut), ('/donations', Donations), ('/error', ErrorPage)])
