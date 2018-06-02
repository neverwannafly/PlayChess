"use strict";
function loadingGif(){
	var a=document.getElementById("firstName").value;
	var b=document.getElementById("lastName").value;
	var c=document.getElementById("username").value;
	var d=document.getElementById("emailID").value;
	var e=document.getElementById("exampleInputPassword1").value;
	var f=document.getElementById("exampleInputPassword2").value;
	var valid_emailID=1;
	var x = d;
    	var atpos = x.indexOf("@");
    	var dotpos = x.lastIndexOf(".");
	if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length) {
        	valid_emailID=0;
    	}
							
	if(a!="" && b!="" && c!="" && d!="" && e!="" && f!="" && valid_emailID==1){
		$("#loading").show();
	}
}
