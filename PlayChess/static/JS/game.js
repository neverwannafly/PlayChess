(function(){

    $(document).ready(function(){

        const window_url = window.location.href;
        const game_index = window_url.indexOf('game/') + 4;
        const game_socket = io.connect(window_url.slice(0, game_index));
        let initial_pos, final_pos;
        let squares = null;
        const game_url = window.location.pathname.split('/')[2];

        game_socket.on('connect', () => {
            game_socket.emit('user_connect', "User has connected!");
        });

        game_socket.on('make_move', move => {
            if (move["success"]) {
                make_move(move['changes']);
            }
            else {
                console.log("Invalid Move!");
            }
        });

        game_socket.on('user_connect', data => {
            console.log(data);
        });

        $(document).on('click', '.square', (event) => {
            const target = $(event.target);
            if(incrementClick()%2!=0) {
                initial_pos = $(target).attr('id');
                    $("#"+initial_pos).addClass("active-cell");
                const move_url = `${game_url}/generateLegalMoves/${initial_pos}`;
                $.ajax({
                    url: move_url,
                })
                .done( (data)=> {
                    squares = data['moves'];
                    highlightSquares(squares);
                });
            }
            else {
                final_pos = $(target).attr('id');
                const move_url = `${game_url}/makemove/${initial_pos}-${final_pos}`;
                $.ajax({
                    url: move_url,
                })
                .done( (data) => {
                    if (data["success"]) {
                        make_move(data['changes']);
                    }
                    else {
                        console.log("Invalid Move!");
                    }
                    game_socket.emit('make_move', {
                        'game_url': game_url, 
                        'init_pos': initial_pos, 
                        'final_pos': final_pos
                    });
                    removeHighlight(squares);
                    $("#"+initial_pos).removeClass("active-cell");
                });
            }
        });

        $("td").hover(mouseIn, mouseOut);

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
    
    });

    function make_move(changes) {
        for (var i=0; i<changes.length; i++) {
            const square_id = "#" + changes[i]['pos'];
            const square_class = changes[i]['class'];
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

    var incrementClick = ( () => {
        var counter = 0;
        return function() {
            return counter += 1;
        }
    })();

})();