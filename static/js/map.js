var OPEN_STATIONS = 5;
var max_stations = 5;
var losers = [];
var open_tables = [];
var playing_players = [];
var CURRENT_MATCHES = [];
var list_of_matches = [];
$(function(){
    $("#footer-body").hide();
});

$(function() {
  $( ".draggable" ).draggable();
  $( ".resizable" ).resizable();
  $( ".draggable3" ).draggable({ containment: "#containment-wrapper", scroll: false });
});

$(function(){
    $("#footer-body").hide();
});

$(function() {
  $( ".draggable" ).draggable();
  $( ".resizable" ).resizable();
  $( ".draggable3" ).draggable({ containment: "#containment-wrapper", scroll: false });
});

function startFirst(data) {
	for (var i=0; i < OPEN_STATIONS; i++) {
		var player1_id = data[i].player1_id;
		var player2_id = data[i].player2_id;
		var match_id = data[i].id;
		var winner_id = data[i].winner_id;
		var loser_id = data[i].loser_id;
		var match = { match_id: match_id, player1_id: player1_id, player2_id: player2_id, winner_id: winner_id, loser_id: loser_id };
		CURRENT_MATCHES.push(match);
	};
	for (var i=0; i < data.length; i++) {
		var player1_id = data[i].player1_id;
		var player2_id = data[i].player2_id;
		var match_id = data[i].id;
		var winner_id = data[i].winner_id;
		var loser_id = data[i].loser_id;
		var match = { match_id: match_id, player1_id: player1_id, player2_id: player2_id, winner_id: winner_id, loser_id: loser_id };
		list_of_matches.push(match);
	};
};
$('#demo').on('click', startDemo);
$('#demo').on('click', live);

function live() {
	$('.live-tournament').html('');
	$('#containment-wrapper').append("<span class='live-tournament'><span class='circle'></span><b>LIVE</b></span>");
	$('.live-tournament').show();
	$('#congrats').text('');
	$('.all-players').css({'color':'white'});
};

function startDemo() {
	$.get('/mock-json', function(data) {
		CURRENT_MATCHES = [];
		startFirst(JSON.parse(data));
			updateTableByTableId(1);
			updateTableByTableId(2);
			updateTableByTableId(3);
			updateTableByTableId(4);
			updateTableByTableId(5);
			clearAndUpdateTables();
	} 
	);
};

function clearAndUpdateTables() {
	var i = 0;
	var table_id;		
	var demo_interval = setInterval(function () {
		if (list_of_matches.length > 0) { 
			table_id = (i%5)+1;
			clearTableByTableId(table_id);
			updateTableByTableId(table_id);
			i++;
		}
		else {
			clearInterval(demo_interval);
			$('.live-tournament').hide();
			$('#table1 .match').text('OPEN');
			$('#indiv-table1 .match').text('OPEN');
			$('#containment-wrapper').append("<span id='congrats'><center>Congratulations, ZeRo!</center></span>");
			
		} 
		}, 2000);
};

var to_be_cleared = [];
function clearTableByTableId(table_id) {
	for (var i=0; i<OPEN_STATIONS; i++) {
		if (($('#table'+(i+1)).attr('id')) == ('table'+table_id)) {
			if ($('#table'+(i+1)+' .match').text() != "OPEN") {
				$('#prev'+(i+1)).text(($('#table'+(i+1)+' .match').text()));
			}
			$('#table'+(i+1)+' .match').text('OPEN');
			$('#indiv-table'+(i+1)+' .match').text('OPEN');
			$('#table'+(i+1)).attr('matchid', '0');
			return (i+1);
		};
	};
};

function updateTableByTableId(table_id) {
	var match = list_of_matches.shift();
	to_be_cleared.push(match);
	var player1_name = players_dict[match['player1_id']];
	var player2_name = players_dict[match['player2_id']];
	var player1_position = playing_players.indexOf(player1_name);
	var player2_position = playing_players.indexOf(player2_name);
	if ((player1_position > -1) && (player2_position > -1)) {
		clearTableByTableId(Math.floor(player1_position/2)+1);
		clearTableByTableId(Math.floor(player2_position/2)+1);
		playing_players[player1_position] = "";
		playing_players[player1_position+1] = "";
		playing_players[player2_position] = "";
		playing_players[player2_position-1] = "";
	}
	
	// Twilio SMS
	if (player1_name == "ZeRo" ) {
		text_message = { text_message: "" + player1_name + ", you're up against " + player2_name + " at Station " + table_id}
		$.post("/twilio", text_message, function (result) {
		}
		);
	}
	else if (player2_name == "ZeRo" ) {
		text_message = { text_message: "" + player2_name + ", you're up against " + player1_name + " at Station " + table_id}
		$.post("/twilio", text_message, function (result) {
		}
		);
	}
	// end Twilio SMS
	$('#table' + table_id + ' .match').text(players_dict[match['player1_id']] + ' vs. ' + players_dict[match['player2_id']]);

	$('#'+players_dict[match['loser_id']]).css({'color':'#666'});
	// current seatings
	$('#indiv-table' + table_id + ' .match').text(players_dict[match['player1_id']] + ' vs. ' + players_dict[match['player2_id']]);

	playing_players[(table_id-1)*2] = player1_name;
	playing_players[(table_id-1)*2+1] = player2_name;
};

function addTables(max_stations) {
	for (var i = 1; i <= max_stations ; i++) {
		$('#containment-wrapper').append("<div class='draggable resizable draggable3 ui-widget-content' id='table" +i+ "'><h3>Station " + i + "</h3><span class='match'></span></div>");
	};
};

addTables(max_stations);
var p = $( "#table1:first");
var position = p.position();
$( "p:last" ).text( "left: " + position.left + ", top: " + position.top );