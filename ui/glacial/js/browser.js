"use strict";

function update(song) {
    document.getElementById("nowplaying").innerHTML = song;
}

function play_song() {
    document.getElementById("song").innerHTML = "playing!";

    $("#duration").text(printer.duration);
}

var prev_interval;

var current_song;

function play_event(song) {
    printer.play(song);

    if(current_song !== undefined)
    {
        $("#song_"+current_song).css("background-color","rgb(255,255,255)");
    }

    current_song = song;
    $("#song_"+song).css("background-color","rgb(0,100,255)");

    $("#duration").text(printer.duration);

    if(prev_interval != null)
        clearInterval(prev_interval);

    $("#time").text("0:00:00");

    prev_interval = setInterval(function() {
        $("#time").text(printer.time);
    },1000);
}

function stop_event() {
    printer.stop();
    clearInterval(prev_interval);
}

function toggle_play() {
    printer.toggle_play()

    if(printer.is_playing == false)
        clearInterval(prev_interval);
    else
        prev_interval = setInterval(function() {
            $("#time").text(printer.time);
        },1000);
}

function parse_songlist(songs) {
    var i;
    /*for (i = 0; i < songs.length; i++) {
        document.getElementById("song_list").innerHTML += "<div onclick='printer.play("+i+")'>" + songs[i] + "</div>";
    }*/
    document.getElementById("song-names").innerHTML = "blob";
}

$(document).ready(function() {
/*    $( "#volume" ).slider({
        slide: function( event, ui ) {
            printer.setVolume(ui.value);
        },
        value: 100
    });*/

/*    var i, track_object = jQuery.parseJSON(printer.tracks);
    document.getElementById("song-names").innerHTML = "";
    for (i = 0; i < 10; i++) {
        //alert("<div onclick='play_event("+i+")'>" + track_object[i] + "</div>");
        document.getElementById("song-names").innerHTML += "<div id='song_"+i+"' onclick='play_event("+i+")'>" + track_object[i] + "</div>";
    }*/

/*    $( "#track_slider" ).slider({
        slide: function( event, ui ) {
            var i, track_object = jQuery.parseJSON(main_window.tracks);
            document.getElementById("song-names").innerHTML = "";
            for (i = 0; i < 10; i++) {
                //alert("<div onclick='play_event("+i+")'>" + track_object[i] + "</div>");
                document.getElementById("song-names").innerHTML += "<div id='song_"+(i+track_object.length-ui.value)+"' onclick='play_event("+(i+track_object.length-ui.value)+")'>" + track_object[i+track_object.length-ui.value] + "</div>";
            }
        },
        orientation: "vertical",
        min: 10,
        max: track_object.length,
        value: track_object.length
    });*/

    var i, artist_object = jQuery.parseJSON(main_window.artists);
    document.getElementById("artist-names").innerHTML = "";
    var element = document.getElementById("artist-names");
    for (i = 0; i < 20; i++) {
        element.innerHTML += "<div onclick='play_event("+i+")'>" + artist_object[i][1] + "</div>";
    }
});
