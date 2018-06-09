import urllib2, urllib
import HTMLParser

def get_class_html(cookie, id):
    """Retorna um dicionario"""

    url = 'http://sigaa.ufpi.br/sigaa/ufpi/portais/discente/discente.jsf'
    query = {'form_acessarTurmaVirtual':'form_acessarTurmaVirtual',
        'idTurma':id,
        'javax.faces.ViewState':'j_id1',
        'form_acessarTurmaVirtual:turmaVirtual':'form_acessarTurmaVirtual:turmaVirtual',}
    data = urllib.urlencode(query)
    request = urllib2.Request(url, data)
    request.add_header("Cookie", cookie)
    html = urllib2.urlopen(request).read()

    #lista de elementos de atividades nao filtradas
    atividades_list_html_not = html.split('<a id="formAva:j_id_jsp_')
    #lista de lementos filtrados
    activities = []

    for activity_html in atividades_list_html_not:

        activity = {} #activity object

        #Para foruns
        if 'idMostrarForum' in activity_html:

            #extrair nome do forum
            activity_html_i = activity_html.find('return false">') + 14
            activity_html_f = activity_html.find('</a>')
            activity['name'] = activity_html[activity_html_i:activity_html_f]

            #extrair date_hora
            activity_html_i = activity_html.find('<span>') + 6
            #verify if a deadline exist
            if not(activity_html_i == 5):
                activity_html_f = activity_html.find('</div>')
                activity['deadline'] = activity_html[activity_html_i:activity_html_f].replace('\\r', ' ').replace('\\t', '').replace('\\n', ' ').replace('</span>', '')
            else:
                activity['deadline'] = "Nao possui prazo de validade."

            activity['type'] =  'forum'

            #acicionando a lista de atividades
            activities.append(activity)

        #para atividades
        elif 'idEnviarMaterial' in activity_html:
            #extrair nome da atividade
            activity_html_i = activity_html.find('return false">') + 14
            activity_html_f = activity_html.find('</a>')
            activity['name'] = activity_html[activity_html_i:activity_html_f]

            #extrair date_hora
            activity_html_i = activity_html.find('">Inicia em') + 2
            activity_html_f = activity_html.find('</div>')
            activity['deadline'] = activity_html[activity_html_i:activity_html_f].replace('\\r', ' ').replace('\\t', '').replace('\\n', ' ').replace('</span>', '')

            activity['type'] = 'assignment'

            #acicionando a lista de atividades
            activities.append(activity)
    #se atividades forem encontradas entao retorneas, caso nao encontrar, none
    if activities:
        return activities

def get_classes_info(html_home, cookie):
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

        class_obj['activities'] = get_class_html(cookie, class_obj['id'])

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
        user['classes'] = get_classes_info(html, cookie)
        user['cookie'] = cookie


        return user
