"use strict";

$(document).ready(function(){
    $(".flipButton").click(function(){
        $.ajax({
            type: "GET",
            url: "board/flip"
        })
        .done(function(data){
            $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
        })
    });
});