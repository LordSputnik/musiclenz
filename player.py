#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui

import PySide.QtWebKit as WebKit

import gobject
gobject.threads_init()
import gst
import os
import json
import mutagen
import datetime

libraryFolder = "/home/ben/Music/FLAC/CDs"
files = list()
song_names = dict()
song_keys = list()

def GetFileList():
    num_files = 0
    for directory,directories,filenames in os.walk(libraryFolder):
        for filename in filenames:
            if os.path.splitext(filename)[1] == ".flac" or os.path.splitext(filename)[1] == ".ogg":
                filename = os.path.join(directory,filename)
                audio = mutagen.File(filename,easy=True)
                song_names[audio["title"][0]] = filename
                num_files += 1

                if num_files > 500:
                    return

class MediaController(QtCore.QObject):

    sound_req = QtCore.Signal()

    @QtCore.Slot()
    def sound_req_handler(self):
        if self.playing:
            self.sound_req.emit()

    def __init__(self, parent=None):
        super(MediaController, self).__init__(parent)
        self.playing = False
        self.test_string = "Tits."
        self.sound_req.connect(self.sound_req_handler)
        self.player = gst.element_factory_make("playbin2","player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        self.cur_time = 0
        self.player.set_property("volume", 1.0)

    @QtCore.Slot(int)
    def play(self,song):
        global app, view
        self.playing = True
        self.cur_time = 0

        self.player.set_state(gst.STATE_NULL)
        self.player.set_property("uri", "file://"+song_names[song_keys[song]])
        self.player.set_state(gst.STATE_PLAYING)

        #print self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT, 10000000000)

        view.page().mainFrame().evaluateJavaScript("update(\""+song_keys[song]+"\"); null")
        #while(self.playing):
            #print "Request!"
            #app.processEvents()

    def _duration(self):
        self.player.get_state()
        duration = self.player.query_duration(gst.FORMAT_TIME)[0]
        delta = datetime.timedelta(seconds=(duration / gst.SECOND))
        return str(delta)

    duration = QtCore.Property(str, fget=_duration)

    def _time(self):
        self.cur_time += 1
        delta = datetime.timedelta(seconds=self.cur_time)
        return str(delta)

    time = QtCore.Property(str, fget=_time)


    @QtCore.Slot()
    def getTracks(self):
        global song_names,song_keys

        song_keys = song_names.keys()
        song_keys.sort()

        return json.dumps(song_keys)

    tracks = QtCore.Property(str, fget=getTracks)

    @QtCore.Slot()
    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.playing = False

    @QtCore.Slot()
    def toggle_play(self):
        if self.playing:
            self.player.set_state(gst.STATE_PAUSED)
        else:
            self.player.set_state(gst.STATE_PLAYING)

        self.playing = not self.playing;

    def _playing(self):
        return self.playing

    is_playing = QtCore.Property(bool, fget=_playing)

    @QtCore.Slot()
    def quit(self):
        global app
        self.player.set_state(gst.STATE_NULL)
        app.quit()

    @QtCore.Slot(int)
    def setVolume(self, value):
        self.player.set_property("volume", pow(float(value)/100.0,2.0))

    @QtCore.Slot(str)
    def print_msg(self, message):
        print message


app = QtGui.QApplication(sys.argv)

controller = MediaController()

view = WebKit.QWebView()
GetFileList()
view.setFixedSize(1024,768)
view.load("./ui/glacial/html/browser.html")
view.page().mainFrame().addToJavaScriptWindowObject('printer',controller)
view.show()

#print "parse_songlist("+json.dumps(files)+"); null"
#view.page().mainFrame().evaluateJavaScript("parse_songlist(['test']); null")

app.exec_()
sys.exit()
