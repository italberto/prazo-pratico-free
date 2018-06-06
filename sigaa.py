import urllib2, urllib

def generate_new_cookie():
    """return a valid virgin cookie"""
    response = urllib2.urlopen('https://sigaa.ufpi.br/sigaa/verTelaLogin.do')
    print response.info()['Set-Cookie']
    return response.info()['Set-Cookie']

def login(username, password):
    cookie = generate_new_cookie().split(';')[0]
    url = 'http://sigaa.ufpi.br/sigaa/logar.do?dispatch=logOn'
    query = {'user.login':username, 'user.senha':password}
    data = urllib.urlencode(query)

    request = urllib2.Request(url, data)
    request.add_header("Cookie", cookie)

    html = urllib2.urlopen(request).read()

    if "rio e/ou senha inv" not in html:
        return html
