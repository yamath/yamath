/*global $*/
/*global MathJax*/
function sendEnvelope() {
    let text = prompt("Puoi inserire un messaggio per descrivere il problema:");
    $.post(
        "/bloomerprofile/ajax/sendEnvelope/",
        {
            'senderUsername': localStorage['bloomerUsername'],
            'receiverUsername': 'admin',
            'serieSerial':localStorage['serieSerial'],
            'topicSerial':localStorage['topicSerial'],
            'questionSerial':localStorage['questionSerial'],
            'answer':localStorage['answer'],
            'text':text},
        function (data) {
            alert("Messaggio inviato. Grazie per la collaborazione.");
        }
    );
}
function deleteEnvelope(pk) {
    $.post(
        "/bloomerprofile/ajax/deleteEnvelope/",
        {'pk':String(pk)},
        function (data) {
            loadEnvelopes(localStorage['bloomerUsername']);
            alert("Messaggio cancellato.");
        }
    );
}
function mathjaxTypeset() {
    MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
}
function loadEnvelopes(bloomerUsername) {
    $.post(
        "/bloomerprofile/ajax/loadEnvelopes/",
        {'username': bloomerUsername},
        function (data) {
            $('#envelopes').html(data);
        }
    );
}
function loadDoneSeries(bloomerUsername) {
    $('#doneSeries').hide();
    $.post(
        "/bloomerprofile/ajax/loadDoneSeries/",
        {'username': bloomerUsername},
        function (data) {
            $('#doneSeries').html(data);
            $('#doneSeries').show();
        }
    );
}
function loadTodoSeries(bloomerUsername) {
    $('#todoSeries').hide();
    $.post(
        "/bloomerprofile/ajax/loadTodoSeries/",
        {'username': bloomerUsername},
        function (data) {
            $('#todoSeries').html(data);
            $('#todoSeries').show();
        }
    );
}
function loadLateSeries(bloomerUsername) {
    $.post(
        "/bloomerprofile/ajax/loadLateSeries/",
        {'username': bloomerUsername},
        function (data) {
            $('#lateSeries').html(data);
            $('#lateSeries').show();
        }
    );
}
function loadQuestionText(bloomerUsername, questionSerial) {
    $.post(
        "/bloomerprofile/ajax/loadQuestionText/",
        {'username': bloomerUsername, 'questionSerial': questionSerial},
        function (data) {
            $('#questionDisplayText').html(data);
        }
    );
}
function loadQuestionForm(bloomerUsername, questionSerial) {
    $.post(
        "/bloomerprofile/ajax/loadQuestionForm/",
        {'username': bloomerUsername, 'questionSerial': questionSerial},
        function (data) {
            $('#questionDisplayForm').html(data);
            $('#questionDisplayFormInput').keypress(function (event) {
                var keycode = event.keyCode || event.which;
                if (keycode == '13') {
                    submitAnswer(bloomerUsername, questionSerial, $('#questionDisplayFormInput').val());    
                }
            });
        }
    );
}
function selectSerie(bloomerUsername, serieSerial) {
    $(window).bind('beforeunload', function(){
        confirm('Abbandonando la pagina in questo momento la domanda risulterà senza risposta. Desideri abbandonare?');
    });
    $('#messageDisplayDjango').hide()
    localStorage['serieSerial']=serieSerial;
    localStorage['answer']='none';
    $.post(
        "/bloomerprofile/ajax/chooseQuestion/",
        {'username':bloomerUsername, 'serieSerial':serieSerial},
        function(data){
            localStorage['questionSerial']=data;
            $.post(
                "/bloomerprofile/ajax/unansweredQuestion/",
                {'username':bloomerUsername, 'questionSerial':data},
                function(data2){
                    localStorage['topicSerial']=data2
                    return false;
                }
            );
            loadQuestionText(bloomerUsername, data);
            loadQuestionForm(bloomerUsername, data);
            $('#messageDisplay').hide();
            $('#questionDisplay').show(callback=function () {MathJax.Hub.Queue(['Typeset',MathJax.Hub]);});
            $('#seriesIndex').hide();
        }
    );
    MathJax.Hub.Queue(['Typeset',MathJax.Hub]);
}
function submitAnswer(bloomerUsername, questionSerial, answer) {
    localStorage['answer']=answer;
    $.post(
        "/bloomerprofile/ajax/submitAnswer/",
        {'username':bloomerUsername, 'questionSerial':questionSerial, 'answer':answer},
        function(data){
            loadDoneSeries(bloomerUsername);
            loadTodoSeries(bloomerUsername);
            loadLateSeries(bloomerUsername);
            if (data == 'true') {
                $('#messageDisplaySuccess').show();
                $('#messageDisplaySuccess').html('Risposta esatta!');
                $('#messageDisplayError').hide();
            } else {
                $('#messageDisplayError').show();
                $('#messageDisplayError').html('Risposta sbagliata!<br /><br />Tu hai risposto: ' + answer + "<br />Una possibile risposta esatta sarebbe stata: " + data);
                $('#messageDisplaySuccess').hide();                
            }
            $('#questionDisplay').hide();
            $('#messageDisplay').show();
            $('#seriesIndex').show();
            $(window).off('beforeunload');
        }
    );
}

// function ajaxPost(request, bloomerUsername) {
//     let returnData = {};
//     $.post(
//         "/bloomerprofile/ajax/",
//         {'request':request, 'username':bloomerUsername},
//         function (ajaxReturnedData) {
//             var keys = [];
//             for(var k in ajaxReturnedData) {
//                 returnData[k]= ajaxReturnedData[k];
//             }
//         },
//         'json');
//     alert(returnData);
//     alert(returnData['doneSeries']);
//     return returnData;
// };