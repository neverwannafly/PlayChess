"use strict"

$(document).ready(function() {
	$("#reg_submit").click(function() {
	// To Display progress bar
		$("#loading7").show();
 		function(status) {
			$("#loading7").hide(); // To Hide progress bar
			alert(status);
		});
	});
});