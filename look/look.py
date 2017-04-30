__pragma__ ('alias', 'S', '$')

def clean(*args):
    for id in args:
        S("#{}".format(id)).empty()

def hide(*args):
    for id in args:
        S("#{}".format(id)).hide()

def hookLogin():
    hide('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard')
    username = back.login()
    clean('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard')
    if not username:
        loadMessage('badnews', "Non è stato possibile accedere. Ritenta o contatta il tuo insegnante.")
        show('badnews')
    load('navbar', 'command=navbar;username={}'.format(username))
    load('welcomeBoard', 'command=welcomeBoard;username={}'.format(username))
    show('navbar', 'welcomeBoard')
    
def hookLogout():
    clean('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard')
    back.logout()
    show('loadingBoard')
    load('navbar', 'command=navbar')
    load('welcomeBoard', 'command=welcomeBoard')
    show('welcomeBoard')
    hide('loadingBoard')
    
def load(id, query):
    print('load', id, query)
    clean(id)
    S.ajax({
        'method': 'GET',
        'url':'html/{}'.format(query),
        'success': lambda d: S("#{}".format(id)).html(d),
        'error': lambda d: load(id, "command=error"),})

def loadMessage(id, msg):
    load(id, 'command=message;message={}'.format(encodeURIComponent(msg)))
    
def show(*args):
    for id in args:
        S("#{}".format(id)).show()

username = S.cookie('username')
load('navbar', 'command=navbar;username={}'.format(username))
load('welcomeBoard', 'command=welcomeBoard;username={}'.format(username))
show('welcomeBoard')
hide('loadingBoard')

