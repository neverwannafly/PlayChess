"use strict";

(function(){
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

        $(document).on('click', '.square', (event) => {
            const target = $(event.target);
            if(incrementClick()%2!=0) {
                initial_pos = $(target).attr('id');
            }
            else {
                final_pos = $(target).attr('id');
                const url = "makemove/" + initial_pos + "-" + final_pos;
                $.ajax({
                    url: url,
                })
                .done( (data) => {
                    if (data["success"]) {
                        make_move(data['changes']);
                    }
                    else {
                        console.log("Invalid Move!");
                    }
                });
            }
        });

        $("td").hover(mouseIn, mouseOut);

    });

    function make_move(changes) {
        for (var i=0; i<changes.length; i++) {
            const square_id = "#" + changes[i]['pos'];
            const square_class = changes[i]['class'];
            $(square_id).removeClass("white-K white-Q white-R white-B white-N white-p black-K black-Q black-R black-B black-N black-p none-_");
            $(square_id).addClass(square_class);
        }
    }

    function mouseIn() {
        const square = $(this).find('.square');
        if (!$(square).hasClass("none-_") || $(square).hasClass("active-square")) {
            square.addClass("highlighted-cell");
        }
    }

    function mouseOut() {
        $(this).find('.square').removeClass("highlighted-cell");
    }

    var incrementClick = (function(){
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();