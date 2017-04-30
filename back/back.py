__pragma__ ('alias', 'S', '$')

def login():
    username = S("input[name='username']").val()
    password = S("input[name='password']").val()
    def httpGet(theUrl):
        xmlHttp = __new__(XMLHttpRequest)
        xmlHttp.open("GET", theUrl, False )
        xmlHttp.send(None)
        return xmlHttp.status
    if httpGet('back/command=login;username={};password={}'.format(username, password)) == 200:
        S.cookie('username', username)
        return username
    else:
        return False
#    def success(d):
#        S.cookie('username', username)
#    def error(d):
#        look.load('messageBoard', 'command=notlogin')
#    S.ajax({
#        'method': 'GET',
#        'url':'back/command=login;username={};password={}'.format(username, password),
#        'success': success,
#        'error': error,})

def logout():
    S.removeCookie('username')
    