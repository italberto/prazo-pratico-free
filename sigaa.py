import urllib2

def generate_new_cookie():
    """return a valid virgin cookie"""
    response = urllib2.urlopen('https://sigaa.ufpi.br/sigaa/verTelaLogin.do')
    return response.info()['Set-Cookie']

def login(cookie, username, password):
    """"""
    query_args = { 'q':'query string', 'foo':'bar' }

    # This urlencodes your data (that's why we need to import urllib at the top)
    data = urllib.urlencode(query_args)

    # Send HTTP POST request
    request = urllib2.Request(url, data)

    response = urllib2.urlopen(request)

    html = response.read()

    # Print the result
    print html
