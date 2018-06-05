"use strict";

$(document).ready(function() {
    // On click signup, hide login and show registration form!
    $("#signup").click(function(){
        $("#login-form").slideUp("slow", function(){
            $("#register-form").slideDown("slow");
        });
    });
    $("#signin").click(function(){
        $("#register-form").slideUp("slow", function(){
            $("#login-form").slideDown("slow");
        });
    });
    $("#registerButton").click(function(event){
        event.preventDefault();
        $(".loader").show();
        $("#load-registration-form").submit();
    })
});