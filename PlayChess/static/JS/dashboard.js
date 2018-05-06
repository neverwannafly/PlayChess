$(document).ready(function(){
    $("tr").hover(function(){
        $(this).children(".normal-cell").css("background-color", "pink");
        $(this).children(".hidden-cell").css("visibility", "visible");
    }, function() {
        $(this).children(".hidden-cell").css("visibility", "hidden");
        $(this).children(".normal-cell").css("background-color", "white");
    });

    $(".deleteButton").click(function(){
        var username = $(this).val();
        $(".hidden-form").val(username);
        $("#exampleModalLabel").text("Delete user " + username + " ?");
    })

});