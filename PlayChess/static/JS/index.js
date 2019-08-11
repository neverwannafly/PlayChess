"use strict";

(function(){

    $(document).ready(function() {

        $(".game-loader").hide();
        $(".main-page-loader").hide();

        $("#find-game").click(function(){
            $(".main").hide();
            $("body").css("background-color", "black");
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
                        $("body").css("background-color", "rgb(29, 29, 29)");
                        $(".main").show();
                    });
                }
            });
        });
    });

})();