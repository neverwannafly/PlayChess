"use strict";

(function(){

    let check_square = null;
    let configuration = true;
    let engineEval = false;
    let strength = 1;

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

        $(".board-left").on('click', function(){
            const default_branch = 0;
            configuration = configuration | 0;
            $.ajax({
                type: "GET",
                url: `board/getPrevState/${default_branch}/${configuration}`,
            })
            .done(function(data) {
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
                if (engineEval) {
                    setEngineEvaluation();
                }
            });
        });

        $(".board-right").on('click', function(){
            const default_branch = 0;
            configuration = configuration | 0;
            $.ajax({
                type: "GET",
                url: `board/getNextState/${default_branch}/${configuration}`,
            })
            .done(function(data) {
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
                if (engineEval) {
                    setEngineEvaluation();
                }
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
                if (engineEval) {
                    setEngineEvaluation();
                }
            });
        });

        $(".board-eval").on('click', function(){
            engineEval = !engineEval;
            if (engineEval) {
                setEngineEvaluation();
                $(".board-eval").addClass('btn-danger');
                $(".board-eval").removeClass('btn-dark');
            } else {
                cleanEngineEval();
                $(".board-eval").addClass('btn-dark');
                $(".board-eval").removeClass('btn-danger');
            }
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
                        if (engineEval) {
                            setEngineEvaluation();
                        }
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

    function parseEval(evaluation) {
        const sign = evaluation[0];
        if (sign=='+') {
            return Number(evaluation.substring(1));
        } else if (sign=='#') {
            const mag = evaluation[1];
            return mag=='+' ? 800 : -800;
        }
        return -1 * Number(evaluation.substring(1));
    }

    function addDecimal(evaluation) {
        const sign = evaluation[0];
        if (sign=='#') {
            return `#${evaluation.substring(2)}`;
        }
        evaluation = Number(evaluation.substring(1));
        evaluation /= 100;
        return `${sign}${evaluation}`;
    }

    function cleanEngineEval() {
        $("#black-eval").text(``);
        $("#white-eval").text(``);
        $("#white-eval").css("width", `50.5%`);
        $("#black-eval").css("width", `50.5%`);
    }

    function setEngineEvaluation() {
        $.ajax({
            type: "GET",
            url: "board/generateFenNotation",
        })
        .done(function(data){
            $.ajax({
                type: "GET",
                url: "api/stockfish",
                data: {
                    token: "hello",
                    fen_notation: data.notation,
                    strength: strength,
                }
            })
            .done(function(data){
                // Flush old eval
                cleanEngineEval();

                // Get new eval
                const maxThreshold = 800;
                let evaluation = parseEval(data.evaluation);
                console.log(data);
                let sign = evaluation > 0 ? 1: -1;
                evaluation = Math.min(Math.abs(evaluation), maxThreshold);
                const relativeEval = (evaluation/maxThreshold);
                let width = 50 * (1 + relativeEval);
                width = Math.ceil(width);
                if (evaluation===0) {
                    $("#white-eval").css("width", `50.5%`);
                    $("#black-eval").css("width", `50.5%`);
                    $("#white-eval").text(`0`);
                    $("#black-eval").text(`0`);
                } else if (sign > 0) {
                    // increase width by relativeEval in favor of white
                    $("#white-eval").css("width", `${width+1}%`);
                    $("#black-eval").css("width", `${101-width}%`);
                    $("#white-eval").text(`${addDecimal(data.evaluation)}`);
                } else {
                    // increase width by relativeEval in favor of black
                    $("#white-eval").css("width", `${101-width}%`);
                    $("#black-eval").css("width", `${width+1}%`);
                    $("#black-eval").text(`${addDecimal(data.evaluation)}`);
                }
            });
        });
    }

    var incrementClick = (function(){
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();