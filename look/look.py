__pragma__ ('alias', 'S', '$')

def clean(*args):
    for id in args:
        S("#{}".format(id)).empty()

def hide(*args):
    for id in args:
        S("#{}".format(id)).hide()

#def hookLogin():
#    hide('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard')
#    username = back.login()
#    clean('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard')
#    if not username:
#        loadMessage('badnews', "Non è stato possibile accedere. Ritenta o contatta il tuo insegnante")
#        show('badnews')
#    load('navbar', 'command=navbar&username={}'.format(username))
#    load('welcomeBoard', 'command=welcomeBoard&username={}'.format(username))
#    show('navbar', 'welcomeBoard')
    
#def hookLogout():
#    clean('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard')
#    back.logout()
#    show('loadingBoard')
#    load('navbar', 'command=navbar')
#    load('welcomeBoard', 'command=welcomeBoard')
#    show('welcomeBoard')
#    hide('loadingBoard')

def hookProfile():
    clean('goodnews', 'badnews', 'welcomeBoard')
    hide('goodnews', 'badnews', 'welcomeBoard')
    load('activeBoard', 'command=profile')
    show('activeBoard')

#def hookSignup():
#    print('hookSignup')
#    hide('navbar', 'goodnews', 'badnews', 'welcomeBoard', 'activeBoard')
#    if back.signup():
#        loadMessage('goodnews', "Il profilo è stato creato e una mail con il link di verifica ti aspetta nella casella di posta")
#        show('goodnews')
#    else:
#        loadMessage('badnews', "Non è stato possibile creare il profilo")
#        show('badnews')
#    load('navbar', 'command=navbar&username={}'.format(username))
#    load('welcomeBoard', 'command=welcomeBoard&username={}'.format(username))
#    show('navbar', 'welcomeBoard')
#    return False
        
    
def load(id, query):
    print('load', id, query)
    clean(id)
    S.ajax({
        'method': 'GET',
        'url':'html/?{}'.format(query),
        'success': lambda d: S("#{}".format(id)).html(d),
        'error': lambda d: load(id, "command=error"),})

def loadMessage(id, msg):
    load(id, 'command=message&message={}'.format(encodeURIComponent(msg)))
    
def show(*args):
    for id in args:
        S("#{}".format(id)).show()

load('navbar', 'command=navbar')
load('welcomeBoard', 'command=welcomeBoard')
show('welcomeBoard')
hide('loadingBoard')

