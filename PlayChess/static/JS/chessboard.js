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
    $("td").click(function(){
        var init_cell_id = $(this).find("div").attr("id");
        $("td").click(function(){
            var final_cell_id = $(this).find("div").attr("id");
            var parameter = init_cell_id + "-" + final_cell_id;
            $.ajax({
                type: "GET",
                url: "makemove/" + parameter
            })
            .done(function(data){
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
            })
        })
        // filter: brightness(70%);
    })
});