import os.path

class Library:

    def __init__(self, lib_id, db_con):

        cur = db_con.cursor()

        cur.execute("SELECT name, directory FROM libraries WHERE id=?",(lib_id,))
        row = cur.fetchone()

        self.directory = row["directory"]
        self.name = row["name"]

        cur.execute("SELECT title FROM songs WHERE library=?",(lib_id,))
        rows = cur.fetchall()

        self.songs = list()

        for row in rows:
            self.songs.append(dict())
            for key in row.keys():
                self.songs[-1][key] = row[key]

    def Scan(self):
        print self.name, repr(self.directory)
        for directory, directories, filenames in os.walk(self.directory):
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                print ext
        return
