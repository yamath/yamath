from content.models import *
from bloomerprofile.models import *
from random import choice

def get_status_of_serie(bloomer, s):
    if isinstance(s, Serie):
        serie = s
    else:
        serie = get_or_none(Serie, serial=s)
    if bloomer.get_mean_of_serie(serie) > 0.9:
        return 'done'
    elif all(get_status_of_serie(bloomer, _s)=='done' for _s in serie.antes):
        return 'todo'
    else:
        return 'late'

def get_series(bloomer, status=None):
    if status is None:
        return list({ serie for classroom in bloomer.classrooms  for serie in classroom.series})
    else:
        return list({ serie for classroom in bloomer.classrooms for serie in classroom.series if get_status_of_serie(bloomer, serie)==status })

def ws_nbsp(s):
     return ''.join( '&nbsp;' if c==' ' else c for c in s )

def loadDoneSeries(bloomer):
    return [ "<li>{3:>4.0%} - <a href='#' onClick=\"selectSerie('{0}', '{1}')\">{2}</a></li>".\
        format(bloomer.username, serie.serial, serie.name, bloomer.get_mean_of_serie(serie))
        for serie in get_series(bloomer, 'done') ]

def loadTodoSeries(bloomer):
    return [ "<li>{3:>4.0%} - <a href='#' onClick=\"selectSerie('{0}', '{1}')\">{2}</a></li>".\
        format(bloomer.username, serie.serial, serie.name, bloomer.get_mean_of_serie(serie))
        for serie in get_series(bloomer, 'todo') ]

def loadLateSeries(bloomer):
    return [ "<li>{3:>4.0%} - <a href='#' onClick=\"selectSerie('{0}', '{1}')\">{2}</a></li>".\
        format(bloomer.username, serie.serial, serie.name, bloomer.get_mean_of_serie(serie))
        for serie in get_series(bloomer, 'late') ]

def loadEnvelopes(bloomer):
    return [ "<li>{1}<br /><a href='#' onClick=\"deleteEnvelope({0})\">Cancella</a></li>".\
        format(envelope.pk, envelope.text)
        for envelope in Envelope.objects.filter(receiver=bloomer) ]

def loadQuestionText(bloomer, question):
    return "<div class='col-xs-12'>{}</div>".format(question.text)

def loadQuestionForm(bloomer, question):
    if question.kind == 'b':
        return [
            "<div class='col-xs-6'><button onClick=\"submitAnswer('{}', '{}', '{}')\">Vero</button></div>".format(
                bloomer.username, question.serial, 'true'),
            "<div class='col-xs-6'><button onClick=\"submitAnswer('{}', '{}', '{}')\">Falso</button></div>".format(
                bloomer.username, question.serial, 'false')]
    if question.kind == 'm':
        return "<div class='col-xs-12'>{}</div>".format(''.join([
                "<p><a href='#' onClick=\"submitAnswer('{0}', '{1}', '{2}')\">{3}</a></p>".format(
                    bloomer.username, question.serial, option.text.translate(str.maketrans({'\\':'\\\\'})), option.text)
                 for option in question.get_uptofive() ]))
    if question.kind == 'o':
        return "<div class='col-xs-12'><input id='questionDisplayFormInput' type='text' name='answer' autocomplete='off'/><button onClick=\"submitAnswer('{}', '{}', {})\">Invia</button></form></div>".format(
            bloomer.username, question.serial, "$('#questionDisplayFormInput').val()") #
    return ""