(function(){

    $(document).ready(function(){

        // This Disables the accidental use of backbutton. 
        (function (global) { 
            if(typeof (global) === "undefined") {
                throw new Error("window is undefined");
            }
            var _hash = "!";
            var noBackPlease = function () {
                global.location.href += "#";
        
                global.setTimeout(function () {
                    global.location.href += "!";
                }, 50);
            };
        
            global.onhashchange = function () {
                if (global.location.hash !== _hash) {
                    global.location.hash = _hash;
                }
            };
        
            global.onload = function () {            
                noBackPlease();
        
                // disables backspace on page except on input fields and textarea
                document.body.onkeydown = (event) => {
                    var elm = event.target.nodeName.toLowerCase();
                    if (event.which === 8 && (elm !== 'input' && elm  !== 'textarea')) {
                        event.preventDefault();
                    }
                    // stopping event bubbling up the DOM tree
                    event.stopPropagation();
                };          
            }
        })(window);
    
    });

});