$(".field").hide();
var game_id = -1;

function whoPlay(player) {
    $("#player").text(player);
}

function symbol_by_player_index(index) {
    if (index === 1)  {
        return "x"
    }
    return "o"
}

function setCellValue(cell, value) {
    $(".cell[value="+ cell + "]").text(value);
}

function refreshCells() {
    $(".cell").text("");
}

$(".new-game").on("click", function(event){
    event.preventDefault();
    $.ajax({
        url: "/api/games/",
        type: "POST",
        datatype: "json",
        success: function(json){
            $(".field").show();
            refreshCells();

            $(".new-game").hide();
            whoPlay(json["step"]);
            game_id = json["pk"];
        },
        error: function(json){
            alert(json);
        }
    });
});

function makeMove(position) {
    var player = parseInt($("#player").text());
    $.ajax({
        url: "/api/games/" + game_id,
        type: "PUT",
        data: {
            "player": player,
            "position": position
        },
        datatype: "json",
        success: function(json) {
            setCellValue(position, symbol_by_player_index(player));
            if (json["finished"] != false) {
                if (json["winner"] == 0) {
                    alert('Ничья!')
                } else {
                    alert("Победил игрок " + json["winner"]);
                }
                location.reload();
            } else {
                $(".field").show();
                $(".new-game").hide();
                whoPlay(json["step"]);
            }
        },
        error: function(json) {
            alert(json.responseJSON["error"]);
        }
    });
}
