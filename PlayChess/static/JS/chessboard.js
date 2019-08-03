"use strict";

(function(){

    let check_square = null;
    let configuration = true;

    $(document).ready(function(){
        $(".board-flip").on('click', function(){
            configuration = (!configuration) | 0; // Method to typecast boolean into int
            $.ajax({
                type: "GET",
                url: `board/flip/${configuration}`
            })
            .done(function(data){
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
            });
        });

        $(".board-reset").on('click', function(){
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
                // check for pawn promotion
                let promotion = "";
                if (checkPromotionValidity(initial_pos)) {
                    promotion = "-" + prompt("Type Q/N/B/R");
                }
                const url = "board/makemove/" + initial_pos + "-" + final_pos + promotion;
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

                    // check for game status here
                    const url = "board/getGameStatus";
                    $.ajax({
                        url: url,
                    })
                    .done( (data) => {
                        if (data["status"]==="finished") {
                            alert(`Game ended! Result: ${data["result"]}-${1-data["result"]}, Cause: ${data["cause"]}`);
                        }
                    })
                });
            }
        });

        $("td").hover(mouseIn, mouseOut);

        $(document).on('click', '.promo-square', (event) => {

        })

    });

    function make_move(changes) {
        for (var i=0; i<changes.length; i++) {
            const square_id = "#" + changes[i]['pos'];
            const square_class = changes[i]['class'];
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

    function checkPromotionValidity(initial_pos) {
        let white_pawn = $("#"+initial_pos).hasClass("white-p") && initial_pos[1]==='7';
        let black_pawn = $("#"+initial_pos).hasClass("black-p") && initial_pos[1]==='2';
        return white_pawn || black_pawn;
    }

    function promotePawn(final_pos) {
        // let promotion = "-";
        // const file = final_pos[0];
        // // white color promotion
        // let squares = [];
        // if (final_pos[1]==="8") {
        //     squares = [file+"8", file+"7", file+"6", file+"5"];
        // }
        // // black color promotion
        // else {
        //     squares = [file+"1", file+"2", file+"3", file+"4"];
        // }
        // for (let i=0; i<squares.length; i++) {
        //     $("#"+squares).removeClass("square");
        //     $("#"+squares).addClass("promo-square");
        // }
        // // returns a string indicating the promoted piece
        // return promotion;        
    }

    var incrementClick = (function(){
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();