var page = 0;
var total_page;

var success_action = function(data) {
	page = 0;
	news = data;
	if(data.length % 10 != 0){
		total_page = data.length / 10 +1;
	} else {
		total_page = data.length / 10;
	}
	display(page);
};

$("#nextpage").on("click", function(e){
	e.preventDefault();
	if(page < total_page - 1) {
		page += 1;
		display(page);
	}
});

$("#previouspage").on("click", function(e){
	e.preventDefault();
	if(page > 0) {
		page += -1;
		display(page);
	}
});

$("#ordinary-search").on("click", function ordinary_search(e){
	e.preventDefault();
	$.ajax({
		type: "POST",
		url: "/ordinary_search/",
		data: {
			csrfmiddlewaretoken: csrf_token,
			'keywords': $('#ordinary-key-words').val(),
		},
		success: success_action
	});
});

function grab_selected() {
	var tasks = [];
	$('input:checked').each(function() {
		tasks.push(this.id);
	});
	return tasks;
}



function display(start) {
	$("#results").html("");
	$("#text-field").html("");
	index = 0;
	// data.forEach(function(e)
	news.slice(start,start + 10).forEach(function(e) {
		$("#results").append(
			'<div class="row">' +
				'<div class="col-md-1">' +
					'<a href="#newsModal' + index + '" class="newsfield-link" data-toggle="modal">' +
						'<h3>' + e[0] + '</h3>' +
					'</a>' +
				'</div>' +
				'<div class="col-md-11">'+
					'<h3>' + e[0] + '</h3>'+
					'<a class="btn btn-primary" href="#newsModal' + index + '" data-toggle="modal">View News<span class="glyphicon glyphicon-chevron-right"></span></a>' +
				'</div>' +
			'</div>' + '<hr>'
		);
		$("#text-field").append(
			'<div class="newsfield-modal modal fade" id="newsModal' + index + '" tabindex="-1" role="dialog" aria-hidden="true">' +
				'<div class="modal-content">' +
					'<div class="close-modal" data-dismiss="modal">' +
						'<div class="lr">' +
							'<div class="rl">' +
							'</div>' +
						'</div>' +
					'</div>' +
					'<div class="container">' +
						'<div class="row">' +
							'<div class="col-lg-8 col-lg-offset-2">' +
								'<div class="modal-body">'+
									e[1] +
								'</div>' +
							'</div>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>'
		);

		index += 1;
	});
}
