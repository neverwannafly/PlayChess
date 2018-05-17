$(document).ready(function(){
    $(".flipButton").click(function(){
        $.ajax({
            type: "GET",
            url: "board/flip"
        })
        .done(function(data){
            console.log(data.board);
            $("tbody").replaceWith("<tbody>"+data.board+"</tbody>");
        })
    });
});