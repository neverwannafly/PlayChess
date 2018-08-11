"use strict";

(function(){

    $(document).ready(function(){

        var socket_message = io.connect(window.location.href);

        socket_message.on('connect', function(){
            socket_message.emit('send_message', "User has connected!");
        })

        socket_message.on('send_message', function(msg) {
            $("#messages").append('<li>'+msg+'</li>');
            console.log(msg);
        });

        $('#sendbutton').on('click', function() {
            socket_message.emit('send_message', $('#myMessage').val());
            $('#myMessage').val('');
        });

    });

})();