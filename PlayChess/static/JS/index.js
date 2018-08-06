"use strict";

(function(){

    $(document).ready(function() {

        $(".game-loader").hide();

        $("#find-game").click(function(){
            $(".main").hide();
            $(".game-loader").show();
            $.ajax({
                url: '/find/game',
                type: 'GET'
            })
            .done( (data) => {
                
            });
        })
    });

})();