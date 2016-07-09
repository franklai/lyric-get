$(document).ready(function(){
	// initialize tab
	$("#tabs").tabs();

	/** binding */
	// select url when focus on #url [text input]
	$("#url").bind('click', function(){
		this.select();
	});

	// select lyric all
	$("#select").bind("click", function(e){
		$("#lyric_div > textarea").focus();
		$("#lyric_div > textarea").select();
	});

	// copy lyric

	if (window.clipboardData){
		$("#copy").bind("click", function(e){
			var text = $("#lyric_div > textarea").val();
			window.clipboardData.clearData(); 
			window.clipboardData.setData("Text", text); 
			window.alert("Lyric has copied to Clipboard.");
		});
	} else {
		$("#copy").attr("disabled", "disabled");
	}

	// binding examples URL
	$("#examples a").click(function(e){
		e.preventDefault();

		var url = e.target.href;
		$("#url").val(url);
		$("#btn_submit").submit();
	});

	// submit url to get episode list
	$("#query_form").bind("submit", function(e){
		// no form submit action
		e.preventDefault();

		var url = jQuery.trim($("#url").val());

		// check input
		if (url == "" || url == $("#url").attr("title")) {
			return false;
		}
		
		// show waiting dialog
		$("#btn_submit").attr("disabled", "disabled");
		$("#lyric_div").hide();
		$("#lyric_div > textarea").empty();
		$("#loading_div").html("Loading...");
		$("#loading_div").show();

		// JSON query
		$.getJSON(
			"http://franklai-lyric-get.appspot.com/app",
			{'url': url},
			function(data){
				var lyric = data["lyric"];
				if (!lyric) {
					// failed to get lyric
					$("#loading_div").html('<span style="color: red;">Failed to get lyric. Please contact franklai.</span>');
					$("#btn_submit").removeAttr("disabled");
					return;
				}
				var count = lyric.split("\n");
				//alert(tmp.length);
				//lyric = tmp.join("<br/>");

				//$("#lyric_div > div").html(lyric);
				$("#lyric_div > textarea").val(lyric);
				$("#lyric_div > textarea").css("height", (14*count.length)+"pt");

				$("#loading_div").hide();
				$("#lyric_div").show();
				$("#btn_submit").removeAttr("disabled");
			}
		);
	});

	$("#loading_div").ajaxError(function(event, request, settings){
		$(this).html('<span style="color: red;">Error.</span>');
		$("#btn_submit").removeAttr("disabled");
	});
	
});
