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

    var counter = 0;
    $(".editButton").click(function(){
        var button_class = "." + $(this).val();
        if (counter%2==0) {
            $(button_class).find("div").css("display", "none");
            $(button_class).find(".hidden-form").css("display", "block");
            $(button_class).find(".deleteButton").css("display", "none");
            $(button_class).find(".editButton").text("Update");
            //$(button_class).find(".editButton").attr("type", "submit");
        }
        else {
            $(button_class).find("div").css("display", "block");
            $(button_class).find(".hidden-form").css("display", "none");
            $(button_class).find(".deleteButton").css("display", "block");
            $(button_class).find(".editButton").text("Edit");
            //$(button_class).find(".editButton").attr("type", "button");
        }
        
        return counter += 1;
    });

});