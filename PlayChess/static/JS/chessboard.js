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
        console.log("clicked!");
        if(incrementClick()%2!=0) {
            initial_pos = $(target).attr('id');
            console.log(initial_pos);
        }
        else {
            final_pos = $(target).attr('id');
            console.log(final_pos);
            var url = "makemove/" + initial_pos + "-" + final_pos;
            console.log(url);
            $.ajax({
                url: url,
            })
            .done(function(data){
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
                console.log("done");
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
