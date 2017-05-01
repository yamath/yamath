__pragma__ ('alias', 'S', '$')

def login():
    email = S("input[name='email']").val()
    password = S("input[name='password']").val()
    print('back login', email, password)
    def httpGet(theUrl):
        xmlHttp = __new__(XMLHttpRequest)
        xmlHttp.open("GET", theUrl, False )
        xmlHttp.send(None)
        return (xmlHttp.status, xmlHttp.responseText)
    status, text = httpGet('back/?command=login&email={}&password={}'.format(email, password))
    if status == 200:
        S.cookie('email', email)
        S.cookie('authtoken', text)
        
        return email
    else:
        return False

def logout():
    S.removeCookie('authtoken')
    S.removeCookie('email')

def signup():
    email = S("input[name='email']").val()
    password = S("input[name='password']").val()
    csrfmiddlewaretoken = S("input[name='csrfmiddlewaretoken']").val()
    print("back signup", email, password)
    def httpGet(theUrl):
        xmlHttp = __new__(XMLHttpRequest)
        xmlHttp.open("POST", theUrl, False )
        xmlHttp.setRequestHeader("X-CSRFToken", S.cookie('csrftoken'))
        xmlHttp.send(None)
        return xmlHttp.status
    if httpGet('back/?command=signup&email={}&password={}&csrfmiddlewaretoken={}'.format(email, password, csrfmiddlewaretoken)) == 200:
        return True
    else:
        return False