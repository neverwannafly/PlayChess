"use strict";

$(document).ready(function() {
    $(".button").click(function(){
        alert("Under development!");
    })
    $(".makeMove").click(function(){
        var move = $("#makemoveinput").val();
        console.log(move);
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
        })
    })
});