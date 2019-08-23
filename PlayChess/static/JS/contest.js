"use strict";

(function(){

    let checkSquare = null;
    let isFirstMove = true;
    let activeMoveCell = null;
    let index = 0;
    // const window_url = window.location.href;
    // const url_index = window_url.indexOf('contest/');
    // const contest_code = window_url.slice(url_index + 8);

    $(document).ready(function(){

        var initial_pos, final_pos;
        var squares = null;

        // Send AJAX request to get first puzzle
        $.ajax({
            url: `fetchPuzzle`,
            data: { 'index': index },
        })
        .done(function(data){
            if (data.success) {
                console.log(data.board);
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
                startClock();
            }
        });

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
                        if (checkSquare!==null) {
                            $(checkSquare).removeClass("check");
                            checkSquare = null;
                            saveCheckSquare();
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
                    let url = "board/getGameStatus";
                    $.ajax({
                        url: url,
                    })
                    .done( (data) => {
                        if (data["status"]==="finished") {
                            alert(`Game ended! Result: ${data["result"]}-${1-data["result"]}, Cause: ${data["cause"]}`);
                        }
                    });
                    
                });
            }
        });

        $("td").hover(mouseIn, mouseOut);

        disableBackButton();

    });

    function createAlert(text, type=0) {
        let types = {0: 'danger', 1: 'success', 2: 'primary', 3: 'warning', 4: 'info'};
        $("#alerts").html(`<div class="alert alert-${types[type]} alert-dismissible fade show">
        <button type="button" class="close" data-dismiss="alert">&times;</button>${text}</div>`);
    }

    function make_move(changes) {
        for (var i=0; i<changes.length; i++) {
            const square_id = "#" + changes[i]['pos'];
            const square_class = changes[i]['class'];
            if (square_class.includes("check")) {
                checkSquare = square_id;
                saveCheckSquare();
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

    function disableBackButton() {
        // This Disables the accidental use of backbutton.
        (function (global) { 
            if(typeof (global) === "undefined") {
                throw new Error("window is undefined");
            }
            var _hash = "!";
            var noBackPlease = function () {
                global.location.href += "#";
        
                global.setTimeout(function () {
                    global.location.href += "!";
                }, 50);
            };
        
            global.onhashchange = function () {
                if (global.location.hash !== _hash) {
                    global.location.hash = _hash;
                }
            };
        
            global.onload = function () {            
                noBackPlease();
        
                // disables backspace on page except on input fields and textarea
                document.body.onkeydown = (event) => {
                    var elm = event.target.nodeName.toLowerCase();
                    if (event.which === 8 && (elm !== 'input' && elm  !== 'textarea')) {
                        event.preventDefault();
                    }
                    // stopping event bubbling up the DOM tree
                    event.stopPropagation();
                };          
            }
        })(window);
    }

    function startClock() {

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

    function saveCheckSquare() {
        localStorage.checkSquare = JSON.stringify(checkSquare);
    }

    function loadCheckSquare() {
        checkSquare = JSON.parse(localStorage.checkSquare || null);
        $(`${checkSquare}`).addClass('check');
    }

    function loadSessionVars() {
        loadCheckSquare()
    }

    var incrementClick = (function(){
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();