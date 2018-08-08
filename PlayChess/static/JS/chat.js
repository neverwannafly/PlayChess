"use strict";

(function(){

    $(document).ready(function(){

        const url = window.location.origin;
        var socket = io.connect(url);

        socket.on('connect', function() {
            socket.send('User has connected!');
        });
        socket.on('message', function(msg) {
            $("#messages").append('<li>'+msg+'</li>');
            console.log('Received message');
        });
        $('#sendbutton').on('click', function() {
            socket.send($('#myMessage').val());
            $('#myMessage').val('');
        });

    });

})();