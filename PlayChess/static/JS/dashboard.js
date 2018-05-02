$(document).ready(function() {
    $("#add").click(function() {
        $("#table").hide();
        $("#form").show();
    });
    $("#cancel").click(function(){
        $("#form").hide();
        $("#table").show();
    })
});