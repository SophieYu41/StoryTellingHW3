// start to query the API
$(document).ready(function() {
	get_data();
});

// this function runs every 10 seconds
function get_data() {
	console.log('get new data');
	get_entropy();
	get_rate();
	get_histogram();
	get_probability();
	add_data_to_graph();
	setTimeout(get_data, 10000);
}

// get entropy from API
function get_entropy() {
	$.getJSON($SCRIPT_ROOT + '/entropy', function(data) {
		if(data) {
			$("#entropy").val(data['entropy']);	
		}
	});
}

// get rate from API
function get_rate() {
	$.getJSON($SCRIPT_ROOT + '/rate', function(data) {
		if(data) {
			$("#rate").val(data['rate']);	
		}
	});
}

// get distribution from API
function get_histogram() {
	$.getJSON($SCRIPT_ROOT + '/', function(data) {
		if(data) {
			draw_pie(data['clinton'], data['trump']);	
		}
	});
}

// get probability from API
function get_probability() {
	$.getJSON($SCRIPT_ROOT + '/probability', function(data) {
		if(data) {
			$("#probability").val(data['probability']);	
		}
	});
}

// For Line Graph
var data_x = [];
var data_y = [];

// set layout for Line Graph
var line_layout = {
	xaxis: {
		title: 'time'
	},
	yaxis: {
		title: 'entropy'
	},
	margin: {
		t: 0
	},
	height: 200,
	width: 1000,
	hovermode: 'closest'
};

// draw Line Graph
function draw_graph() {
	var data = [
		{
			x: data_x,
			y: data_y,
			name: 'Entropy'
		},
	];
	Plotly.newPlot('graph', data, line_layout);
}

// add data to Line graph
function add_data_to_graph() {
	$.getJSON($SCRIPT_ROOT + '/entropy', function(data) {
        if(data) {
        	console.log(data);
        	data_x.push(data['time']);
			data_y.push(data['entropy']);
			if(data_y.length > 10) {
				data_x.shift();
				data_y.shift();    
			}
			draw_graph();
			var len = data_y.length;
			console.log(Math.abs(data_y[len-1] - data_y[len-2]));
			if(len > 1 && Math.abs(data_y[len-1] - data_y[len-2]) > 0.02*data_y[len-2]) {
				send_alert(data_x[len-1]);
			}
        }       
	});
}

// define pie chart data
var pie_data = [{
	values: [],
	labels: ['Clinton', 'Trump'],
	type: 'pie'
}];

// set pie chart format
var pie_layout = {
	title: 'Distribution',
	height: 250,
	width: 300,
	margin: {
		t: 40
	},
};

// draw pie chart
function draw_pie(a, b) {
	pie_data[0]['values'] = [a, b];
	Plotly.newPlot('chart', pie_data, pie_layout);
}

// trigger alert
function send_alert(time) {
	$('.messageBox').show(); 
	setTimeout(function() {
		$('.messageBox').hide();
	}, 1000);
	$('#alert').prepend('<li>' + '@ ' + time + ', the Entropy changed > 2% </li>')
}

