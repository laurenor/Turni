function updateCoords() {
  // Gets coordinates from positions table in DB, so gaming stations are in same place when user returns to page later
  $.get('/get-coords', { tournament_name: tournament_name }, function (result) {
    result = JSON.parse(result);
    for (var i = 0; i < max_stations; i++) {       
        $('#'+result[i][0]).css({'position': 'absolute', 'left': result[i][1]+'px', 'top': result[i][2]+'px'});
    }
  }
  )
};
updateCoords();

function reset() {
  // 
  $("#table1").css({'position': 'absolute', 'left': '72px', 'top': '50px', 'width': '162px', 'height':'303px'});
  $("#table2").css({'position': 'absolute', 'left': '309px', 'top': '50px', 'width': '120px', 'height':'120px'});
  $("#table3").css({'position': 'absolute', 'left': '495px', 'top': '50px', 'width': '120px', 'height':'120px'});
  $("#table4").css({'position': 'absolute', 'left': '309px', 'top': '227px', 'width': '120px', 'height':'120px'});
  $("#table5").css({'position': 'absolute', 'left': '495px', 'top': '227px', 'width': '120px', 'height':'120px'});
}
$('#reset').on('click', reset);

function saveToDb() {
  // Adds/updates table coordinates to database.
  for (var i = 1; i <= max_stations; i++) {
    pos = $('#table'+i).position();
    var positions = { left: pos.left, top: pos.top, table_id: "table"+i, tournament_name: tournament_name };
    $.post("/add-coords", positions, function (result) {
        $('#save_status').text(result);
    }
    );
  };
};
$('#save').on('click', saveToDb);