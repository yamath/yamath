/*global $*/
/*global MathJax*/
function mathjaxTypeset() {
    MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
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
                if (keycode === '13') {
                    submitAnswer(bloomerUsername, questionSerial, $('#questionDisplayFormInput').val());    
                }
            });
        }
    );
}
function selectSerie(bloomerUsername, serieSerial) {
    $(window).bind('beforeunload', function(){
        return 'Abbandonando la pagina in questo momento la domanda risulterà senza risposta. Desideri abbandonare?';
    });
    $('#messageDisplayDjango').hide()
    $.post(
        "/bloomerprofile/ajax/chooseQuestion/",
        {'username':bloomerUsername, 'serieSerial':serieSerial},
        function(data){
            window.onunload = function() {
                $.post(
                    "/bloomerprofile/ajax/unansweredQuestion/",
                    {'username':bloomerUsername, 'questionSerial':data},
                    function(data){
                        return false;
                    }
                );
            }
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
                $('#messageDisplayError').html('Risposta sbagliata!');
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