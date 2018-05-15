$(document).ready(function(){

    $("tr").hover(mouseIn, mouseOut);

    $(".deleteButton").click(function(){
        var username = $(this).val();
        $("#exampleModal").find(".hidden-form").val(username);
        $("#exampleModalLabel").text("Delete user " + username + " ?");
    })

    $(".editButton").click(function(event){
        var button_class = "." + $(this).val();
        editButtonPressed(button_class, event);
    });

    $(".updateButton").click(function(event){
        var button_class = "." + $(this).val();
        updateButtonPressed(button_class, event);
    })

    $("form").on("submit", function(event){
        var username_class = "." + $(this).attr("id").split('-')[0];
        $.ajax({
            data : {
                username : $(username_class).find("input[name='username']").val(),
                name : $(username_class).find("input[name='name']").val(),
                email : $(username_class).find("input[name='email']").val(),
                rating : $(username_class).find("input[name='rating']").val(),
                authentication : $(username_class).find("select[name='authentication']").val(),
                image : $(username_class).find("input[name='image']").val()
            },
            type : "POST",
            url : "update"
        })
        .done(function(data){
            var forms = $(username_class).find(".hidden-form");
            var divs = $(username_class).find(".detail");

            var counter = 0;
            for (element in data) {
                forms.eq(counter).val(data[element]);
                divs.eq(counter).text(data[element]);
                counter += 1;
            }
        })
        event.preventDefault();
    })

});

function mouseIn() {
    $(this).children(".normal-cell").css("background-color", "pink");
    $(this).children(".hidden-cell").css("visibility", "visible");
}

function mouseOut() {
    $(this).children(".hidden-cell").css("visibility", "hidden");
    $(this).children(".normal-cell").css("background-color", "white");
}

function editButtonPressed(button, event) {
    $(button).find(".detail").hide();
    $(button).find(".deleteButton").hide();
    $(button).find(".editButton").hide();
    $(button).find(".hidden-form").show();
    $(button).find(".updateButton").show();
}

function updateButtonPressed(button, event) {
    $(button).find(".hidden-form").hide();
    $(button).find(".updateButton").hide();
    $(button).find(".detail").show();
    $(button).find(".deleteButton").show();
    $(button).find(".editButton").show();
}