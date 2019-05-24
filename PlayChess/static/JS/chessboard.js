"use strict";

(function(){

    let check_square = null;

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

        $(".resetButton").on('click', function(){
            $.ajax({
                type: "GET",
                url: "board/reset",
                data: {
                    "fen": "default",
                }
            })
            .done(function(data) {
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
            })
        });

        var initial_pos, final_pos;
        var squares = null;

        $(document).on('click', '.square', (event) => {
            const target = $(event.target);
            if(incrementClick()%2!=0) {
                initial_pos = $(target).attr('id');

                if ($("#"+initial_pos).hasClass("none-_")) {
                    incrementClick();
                } 
                else {
                    $("#"+initial_pos).addClass("active-cell");
                    const url = "board/generateLegalMoves/" + initial_pos;
                    $.ajax({
                        url: url,
                    })
                    .done( (data)=> {
                        squares = data['moves'];
                        highlightSquares(squares);
                    });
                }
            }
            else {
                final_pos = $(target).attr('id');
                const url = "board/makemove/" + initial_pos + "-" + final_pos;
                $.ajax({
                    url: url,
                })
                .done( (data) => {
                    console.log(data);
                    if (!data["gameFinished"] && data["success"]) {
                        console.log(data['changes'])
                        if (check_square!==null) {
                            $(check_square).removeClass("check");
                            check_square = null;
                        }
                        make_move(data['changes']);
                    } else if (data["gameFinished"]) {
                        console.log("Game Finished", data["result"]);
                    }
                    else {
                        console.log("Invalid Move!");
                    }
                    removeHighlight(squares);
                    $("#"+initial_pos).removeClass("active-cell");
                });
            }
        });

        $("td").hover(mouseIn, mouseOut);

    });

    function make_move(changes) {
        for (var i=0; i<changes.length; i++) {
            const square_id = "#" + changes[i]['pos'];
            const square_class = changes[i]['class'];
            console.log(square_id, square_class);
            if (square_class.includes("check")) {
                check_square = square_id;
            }
            $(square_id).removeClass("white-K white-Q white-R white-B white-N white-p black-K black-Q black-R black-B black-N black-p none-_");
            $(square_id).addClass(square_class);
        }
    }

    function highlightSquares(squares) {
        for (var i=0; i<squares.length; i++) {
            const square_id = "#" + squares[i];
            $(square_id).addClass('highlighted-cell');
        }
    }

    function removeHighlight(squares) {
        for (var i=0; i<squares.length; i++) {
            const square_id = "#" + squares[i];
            $(square_id).removeClass('highlighted-cell');
        }
    }

    function mouseIn() {
        const square = $(this).find('.square');
        if (!$(square).hasClass("none-_") || $(square).hasClass("active-square")) {
            square.addClass("hover-cell");
        }
    }

    function mouseOut() {
        $(this).find('.square').removeClass("hover-cell");
    }

    var incrementClick = (function(){
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();