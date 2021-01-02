"use strict";

(function(){

    let isFirstMove = true;
    let activeMoveCell = null;
    let index = 0;

    var endTime;
    var clock;
    // const window_url = window.location.href;
    // const url_index = window_url.indexOf('contest/');
    // const contest_code = window_url.slice(url_index + 8);

    $(document).ready(function(){

        loadSessionVars();

        var initial_pos, final_pos;
        var squares = null;

        // Send AJAX request to get first puzzle
        getPuzzle();
        loadClock();

        $(document).on('click', '.square', (event) => {
            const target = $(event.target);
            if(incrementClick()%2!=0) {
                initial_pos = $(target).attr('id');

                if ($("#"+initial_pos).hasClass("none-_")) {
                    incrementClick();
                } 
                else {
                    $("#"+initial_pos).addClass("active-cell");
                    const url = "generateLegalMoves/" + initial_pos;
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
                const url = "makemove/" + initial_pos + "-" + final_pos + promotion;
                $.ajax({
                    url: url,
                    data: { index: index },
                })
                .done( (data) => {
                    if (!data["move"]) {
                        console.log("Invalid Move!");
                    } else if (data["success"] && data["puzzleOver"]) {
                        console.log("Puzzle solved successfully");
                        make_move(data['changes']);
                        index += 1;
                        saveIndexValue();
                        createAlert("Correct", 1);
                        getPuzzle();

                    } else if (!data["success"] && data["puzzleOver"]) {
                        console.log("Puzzle Failed!");
                        make_move(data['changes']);
                        index += 1;
                        saveIndexValue();
                        createAlert("Incorrect", 0);
                        getPuzzle();
                    }
                    else {
                        console.log("Correct Move! Keep on going");
                        make_move(data['changes']);
                        createAlert("Keep on Going!", 4);
                    }
                    removeHighlight(squares);
                    $("#"+initial_pos).removeClass("active-cell");
                    
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

    function getPuzzle() {
        $.ajax({
            url: `fetchPuzzle`,
            data: { 'index': index },
        })
        .done(function(data){
            if (data.contest_ended) {
                endContest();
            }
            if (data.success) {
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
            }
        });
    }

    function make_move(changes) {
        for (var i=0; i<changes.length; i++) {
            const square_id = "#" + changes[i]['pos'];
            const square_class = changes[i]['class'];
            $(square_id).removeClass("white-K white-Q white-R white-B white-N white-p black-K black-Q black-R black-B black-N black-p none-_");
            $(square_id).addClass(square_class);
            $(square_id).removeClass('check');
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

    function loadClock() {

        if(endTime===null) {
            endTime = new Date()
            endTime.setMinutes(endTime.getMinutes() + 20);
            endTime = (Date.parse(endTime) / 1000);
            saveEndTime();
        }

        function makeTimer() {

            var now = new Date();
            now = (Date.parse(now) / 1000);

            var timeLeft = endTime - now;
            if (timeLeft<=0) {
                window.clearInterval(clock);
                endContest();
                timeLeft = 0;
            }

            var days = Math.floor(Math.max(timeLeft / 86400), 0); 
            var hours = Math.floor(Math.max((timeLeft - (days * 86400)) / 3600), 0);
            var minutes = Math.floor(Math.max((timeLeft - (days * 86400) - (hours * 3600 )) / 60), 0);
            var seconds = Math.floor(Math.max((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60))), 0);
    
            if (hours < "10") { hours = "0" + hours; }
            if (minutes < "10") { minutes = "0" + minutes; }
            if (seconds < "10") { seconds = "0" + seconds; }

            $("#minutes").html(minutes + "<span>Mins </span>");
            $("#seconds").html(seconds + "<span>Seconds </span>");
        }
        
        clock = setInterval(function() { makeTimer(); }, 1000);
    }

    function loadLeaderboards() {
        let contest_id = window.location.href;
        let base_url = window.location.href;
        base_url = base_url.slice(0, base_url.indexOf('/contest')+8);
        contest_id = contest_id.slice(contest_id.indexOf('contest/')+8);
        contest_id = contest_id.slice(0, contest_id.indexOf('/'));
        window.location.href = `${base_url}/${contest_id}/leaderboards`;
    }

    function endContest() {
        $.ajax({
            url: 'end_contest',
        })
        .done(function(){
            loadLeaderboards();
        });
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

    function saveIndexValue() {
        localStorage.index = JSON.stringify(index);
    }

    function loadIndexValue() {
        index = 0;
    }

    function saveEndTime() {
        localStorage.endTime = JSON.stringify(endTime);
    }

    function loadEndTime() {
        endTime = null;
    }

    function loadSessionVars() {
        loadIndexValue()
        loadEndTime();
    }

    var incrementClick = (function(){
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();