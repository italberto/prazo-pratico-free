import urllib2, urllib

def get_classes_info(html_home):
    """return classes objects exhtracted from homepage_html"""
    #list of class elements
    classes = []
    classes_html_elements = html_home.split('<input type="hidden" name="form_acessarTurmaVirtual')[1:]

    for class_html in classes_html_elements:
        class_obj = {} # class object
        #class id extrating
        class_html_i = class_html.find('<input type="hidden" value="') + 28
        class_html_j = class_html.find('" name="idTurma" />')
        class_obj['id'] = class_html[class_html_i:class_html_j]

        #class name extrating
        class_html_i = class_html.find('return false">') + 14
        class_html_j = class_html.find('</a><input type="hidden"')
        class_obj['name'] = class_html[class_html_i:class_html_j]

        classes.append(class_obj)
    return classes

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

    if ("rio e/ou senha inv" not in html) and 'username: "' in html:
        #user object
        user = {}

        username_i = html.find('username: "') + 11
        username_f = html.find('", //pode ser retornado por funcao ou uma string')

        user['username'] = html[username_i:username_f]
        user['classes'] = get_classes_info(html)

        return user
