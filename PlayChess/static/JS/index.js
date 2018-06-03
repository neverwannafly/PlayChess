"use strict";

$(document).ready(function() {
    $(".button").click(function(){
        alert("Under development!");
    })
    $(".makeMove").click(function(){
        sendAjaxRequest();
    })
    $("#makemoveinput").keyup(function(e){
        if (e.which==13) {
            sendAjaxRequest();
        }
    })
});

function sendAjaxRequest() {
    var move = $("#makemoveinput").val();
    $.ajax({
        type: "GET",
        url: "makemove/"+move,
        error : function(xhr, status, error) {
            alert("Please enter a valid move!");
            },
    })
    .done(function(data){
        $("iframe").contents().find("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
        $("#makemoveinput").val("");
    });
}