"use strict";

function update(song) {
    document.getElementById("nowplaying").innerHTML = song;
}

function play_song() {
    document.getElementById("song").innerHTML = "playing!";

    $("#duration").text(printer.duration);
}

var prev_interval;

function play_event(song) {
    printer.play(song);

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
    document.getElementById("song-list").innerHTML = "blob";
}

$(document).ready(function() {
    $( "#volume" ).slider({
        slide: function( event, ui ) {
            printer.setVolume(ui.value);
        },
        value: 100
    });

    var i, track_object = jQuery.parseJSON(printer.tracks);
    document.getElementById("song-list").innerHTML = "";
    for (i = 0; i < track_object.length; i++) {
        //alert("<div onclick='play_event("+i+")'>" + track_object[i] + "</div>");
        document.getElementById("song-list").innerHTML += "<div onclick='play_event("+i+")'>" + track_object[i] + "</div>";
    }
});