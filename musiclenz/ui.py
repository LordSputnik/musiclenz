from PySide import QtCore

import sqlite3 as db
import json

local_db = db.connect("test.db")
local_db.row_factory = db.Row

class MainWindow(QtCore.QObject):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.artist_limits = (20, 0)

    def setArtistListLimits(self, offset, limit = 20):
        self.artist_limits = (limit, offset)

    def getArtists(self):
        cur = local_db.cursor()

        cur.execute("SELECT id, name FROM artists ORDER BY name ASC LIMIT ? OFFSET ?", self.artist_limits)
        results = cur.fetchall()

        return json.dumps([(result[0], result[1]) for result in results])

    artists = QtCore.Property(str, fget = getArtists)

    def onClickSong(self):
        pass

    def onClickPlay(self):
        pass

    def onSetVolume(self):
        self.player.set_property("volume", pow(float(value) / 100.0, 2.0))

class UIController(QtCore.QObject):
    def __init__(self, view, parent = None):
        super(UIController, self).__init__(parent)
        self.main_window = MainWindow()
        view.page().mainFrame().addToJavaScriptWindowObject('main_window', self.main_window)
