"use strict";

(function(){

    $(document).ready(function() {

        $(".game-loader").hide();

        $("#find-game").click(function(){
            $(".main").hide();
            $(".game-loader").show();
            $.ajax({
                url: '/find_game',
                type: 'GET'
            })
            .done( (data) => {
                if (data['url']) {
                    window.location.assign(`/game/${data['url']}`);
                }
                else {
                    $(".game-loader").hide();
                    swal({
                        type: 'error',
                        title: 'Sorry...',
                        text: 'No other player found! Please try again later.',
                        footer: '<a id="issue-url" href="#">Why do I have this issue?</a>'
                    }).then(function() {
                        $(".main").show();
                    });
                }
            });
        });
    });

})();