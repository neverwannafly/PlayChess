"use strict";

(function(){

    let checkSquare = null;
    let configuration = true;
    let engineEval = false;
    let storyMode = false;
    let strength = 1;
    let isFirstMove = true;
    let states = [];

    $(document).ready(function(){

        $(window).on('reload load onload', function(){
            $(".main").hide();
            $(".main-page-loader").show();
            $("body").css("background-color", "black");
            loadSessionVars();
            setTimeout(function(){
                $(".main-page-loader").hide();
                $(".main").css("display", "flex");
                $("body").css("background-color", "rgb(29, 29, 29)");
            }, 1500);
        });

        $(".board-flip").on('click', function(){
            configuration = (!configuration) | 0; // Method to typecast boolean into int
            saveConfiguration();
            flipBoard();
        });

        $(".board-left").on('click', function(){
            getPrevState();
        });

        jQuery(window).on("swipeleft keydown", function(event) {
            if (event.type=="keydown") {
                if (event.key=="ArrowLeft") {
                    getPrevState();
                }
            } else {
                getPrevState();
            }
        });

        $(".board-right").on('click', function(){
            getNextState();
        });

        jQuery(window).on("swiperight keydown", function(event) {
            if (event.type=="keydown") {
                if (event.key=="ArrowRight") {
                    getNextState();
                }
            } else {
                getNextState();
            }
        });

        $(".board-fen").on('click', function(){
            $.ajax({
                type: "GET",
                url: "board/generateFenNotation",
            })
            .done(function(data){
                console.log(data.notation);
                copyToClipboard(data.notation);
                createAlert("FEN Notation copied to clipboard", 1);
            });
        })

        $(".board-reset").on('click', function(){
            $.ajax({
                type: "GET",
                url: `board/reset`,
                data: {
                    "fen": "default",
                    "configuration": configuration,
                }
            })
            .done(function(data) {
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
                if (engineEval) {
                    setEngineEvaluation();
                }
                resetStates();
            });
        });

        $(".board-story").on('click resize', function(event) {
            if (event.type=="click") {
                storyMode = !storyMode;
                saveStoryMode();
            }
            if (storyMode) {
                engageStoryMode();
            } else {
                dismissStoryMode();
            }
        });

        $(".board-eval").on('click', function(){
            engineEval = !engineEval;
            saveEngineEval();
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

        $("#save-story").on('click', function(){
            // saveStory();
        });

        $("#load-story").on('click', function(){
            // loadStory();
        });

        // Will complete later
        $(".engine-str").on('click', function(){
            strength += 1;
            saveStrength();
        })

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
                        if (checkSquare!==null) {
                            $(checkSquare).removeClass("check");
                            checkSquare = null;
                        }
                        make_move(data['changes']);
                        addMoveToStoryBoard();
                        
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

    });

    function flipBoard() {
        $.ajax({
            type: "GET",
            url: `board/flip/${configuration}`,
        })
        .done(function(data){
            $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
            if (!configuration) {
                $(".board-flip").removeClass("btn-dark");
                $(".board-flip").addClass("btn-info");
            } else {
                $(".board-flip").removeClass("btn-info");
                $(".board-flip").addClass("btn-dark");
            }
        });
    }

    function copyToClipboard(text) {
        let temp = $("<input>");
        $("body").append(temp);
        temp.val(`${text}`).select();
        document.execCommand("copy");
        temp.remove();
    }

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

    function getNextState() {
        const default_branch = 0;
        configuration = configuration | 0;
        $.ajax({
            type: "GET",
            url: `board/getNextState/${default_branch}/${configuration}`,
        })
        .done(function(data) {
            if (data.success) {
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
                if (engineEval) {
                    setEngineEvaluation();
                }
            }
        });
    }

    function getPrevState() {
        // const default_branch = 0;
        configuration = configuration | 0;
        $.ajax({
            type: "GET",
            url: `board/getPrevState/${configuration}`,
        })
        .done(function(data) {
            if (data.success) {
                $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
                if (engineEval) {
                    setEngineEvaluation();
                }
            }
        });
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
        createAlert("Engine is unavailable!", 4);
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

    function engageStoryMode() {
        let width = window.innerWidth;
        if (width <= 531) {
            $(".topbar").hide();
        } else {
            $(".sidebar").hide();
        }
        $("#find-game").hide();
        $(".board-story").addClass("btn-success");
        $(".board-story").removeClass("btn-dark");

        $("#storyboard").css("display", "flex");
    }

    function dismissStoryMode() {
        let width = window.innerWidth;
        if (width <= 531) {
            $(".topbar").show();
        } else {
            $(".sidebar").show();
        }
        $("#find-game").show();
        $(".board-story").addClass("btn-dark");
        $(".board-story").removeClass("btn-success");

        $("#storyboard").hide();
    }

    function makeId(branch, state) {
        return 1000*branch + state;
    }

    function extractFromId(id) {
        let BRANCHING_LIMIT = 1000;
        return {
            branch: id%BRANCHING_LIMIT,
            state: id/BRANCHING_LIMIT,
        }
    }

    function highlightMoveCell(id) {
        $(`#${id}`).addClass('highlight-move-cell');
    }

    function removeMoveCellHighlight(id) {
        $(`#${id}`).removeClass('highlight-move-cell');
    }

    function saveStates() {
        localStorage.states = JSON.stringify(states);
    }

    function loadStates() {
        $.ajax({
            url: "board/getBranchState",
        })
        .done( (data) => {
            states = data;
            saveStates();
            for (let i=0; i<states.length; i++) {
                createMoveDivs(states[i][0], states[i][1], states[i][2]);
            }
        });
    }

    function resetStates() {
        states = [];
        saveStates();
        document.getElementById("move-number").innerHTML = "";
        document.getElementById("white-moves").innerHTML = "";
        document.getElementById("black-moves").innerHTML = "";
    }

    function createMoveDivs(branch, state, notation) {
        const id = makeId(branch, state);

        removeMoveCellHighlight(id-1);

        if (state%2!=0) {
            isFirstMove = false;
            // insert move number
            let move_number_div = `<div class="move-number-cell">${Math.floor((state+1)/2)}</div>`
            document.getElementById("move-number").innerHTML += move_number_div;

            let move_div = `<div id="${id}" class="move-cell">${notation}</div>`;
            document.getElementById("white-moves").innerHTML += move_div;

            highlightMoveCell(id);

            let black_div = `<div id="temp-div" class="move-cell">...</div>`;
            document.getElementById("black-moves").innerHTML += black_div;

            $(".story").scrollTop($(".story")[0].scrollHeight);
        } else {
            if (isFirstMove) {
                let move_number_div = `<div class="move-number-cell">${Math.floor((state+1)/2)}</div>`
                document.getElementById("move-number").innerHTML += move_number_div;

                let blank_div = `<div id="-1" class="move-cell">...</div>`;
                document.getElementById("white-moves").innerHTML += blank_div;

                let move_div = `<div id="${id}" class="move-cell">${notation}</div>`;
                document.getElementById("black-moves").innerHTML += move_div;
            } else {
                isFirstMove = false;
                $("#temp-div").prop('id', `${id}`);
                $(`#${id}`).text(`${notation}`);
            }
            highlightMoveCell(id);
        }
    }

    function addMoveToStoryBoard() {
        let url = "board/getCurrentState";
        $.ajax({
            url: url,
        })
        .done( (data) => {
            let state = data.state;
            let branch = data.branch;
            let notation = data.move;

            createMoveDivs(branch, state, notation);
            // Need to Fix this when adding sub vars
            states.push([branch, state, notation]);
            saveStates();
        });
    }

    function saveStory() {
        $.ajax({
            url: "board/save",
        })
        .done(function(data) {
            console.log("saved!");
        });
    }

    function loadStory() {
        $.ajax({
            url: "board/load",
        })
        .done(function(data) {
            console.log("loading story");
        });
    }

    function saveCheckSquare() {
        localStorage.checkSquare = JSON.stringify(checkSquare);
    }

    function loadCheckSquare() {
        checkSquare = JSON.parse(localStorage.checkSquare || null);
    }

    function saveConfiguration() {
        localStorage.configuration = JSON.stringify(configuration);
    }

    function loadConfiguration() {
        configuration = JSON.parse(localStorage.configuration || true);
        if (!configuration) {
            flipBoard();
        }
    }

    function saveEngineEval() {
        localStorage.engineEval = JSON.stringify(engineEval);
    }

    function loadEngineEval() {
        engineEval = JSON.parse(localStorage.engineEval || false);
        if (engineEval) {
            setEngineEvaluation();
            $(".board-eval").addClass('btn-danger');
            $(".board-eval").removeClass('btn-dark');
        }
    }

    function saveStoryMode() {
        localStorage.storyMode = JSON.stringify(storyMode);
    }

    function loadStoryMode() {
        storyMode = JSON.parse(localStorage.storyMode || false);
        if (storyMode) {
            engageStoryMode();
        }
    }

    function saveStrength() {
        localStorage.strength = JSON.stringify(strength);
    }

    function loadStrength() {
        strength = JSON.parse(localStorage.strength || 1);
    }

    function loadSessionVars() {
        loadCheckSquare();
        loadConfiguration();
        loadEngineEval();
        loadStoryMode();
        loadStrength();
        loadStates();
    }

    var incrementClick = (function(){
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();