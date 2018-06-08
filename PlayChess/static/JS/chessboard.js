"use strict";

$(document).ready(function(){
    $(".flipButton").on('click', function(){
        $.ajax({
            type: "GET",
            url: "board/flip"
        })
        .done(function(data){
            $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
        });
    });

    var initial_pos, final_pos;

    $(document).on('click', '.square', function(e){
        var target = $(e.target), article;
        if(incrementClick()%2!=0) {
            initial_pos = $(target).attr('id');
        }
        else {
            final_pos = $(target).attr('id');
            var url = "makemove/" + initial_pos + "-" + final_pos;
            $.ajax({
                url: url,
                error : function(xhr, status, error) {
                    console.log("Please enter valid move!");
                },
            })
            .done(function(data){
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
            })
        }
    });
});

var incrementClick = (function(){
    var counter = 0;
    return function() {
        return counter += 1;
    }
}) ();
