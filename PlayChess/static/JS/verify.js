"use strict";

(function(){

    $(document).ready(function(){
        $("#verify").click(function(){
            $(".loader").show();
            $("#header-text").text("Resending...");
            $.ajax({
                type: "POST",
                url: window.location.pathname + "/retry",
            })
            .done(function(data){
                $(".loader").hide();
                $("#header-text").text("Verification Code");
                if (data['response']) {
                    $(".success").html(`
                    <div class="alert alert-success alert-dismissible fade show">
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                        <div class="text">Mail successfully sent!</div>
                    </div>
                    `);
                } else {
                    $(".success").html(`
                    <div class="alert alert-danger alert-dismissible fade show">
                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                        <div class="text">There was some problem sending the mail! Please try again later.</div>
                    </div>
                    `);
                }
            })
        })
    });

})();