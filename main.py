import sys

from PyQt6.QtWidgets import QApplication
import toml

from note import Note
from ui import MainWindow, NotesViewer
from db import Database


class Application(QApplication):
    def __init__(self):
        super(Application, self).__init__(sys.argv)

        with open("config.toml", 'r') as file:
            self.config = toml.load(file)

        self.ui = MainWindow()
        self.ui.note_editor.send_note.connect(self.save_data)

        self.test_viewer = NotesViewer(None)
        self.test_viewer.setVisible(True)
        self.test_viewer.start_update.connect(self.test_load_data)

        self.db = Database(self.config["database"]["name"], self.config["database"]["collection"])


    def save_data(self, note: Note):
        self.db.save_note(note)

    def test_load_data(self):
        self.test_viewer\
            .update_notes(self.db.load_notes())



if __name__ == '__main__':
    app = Application()
    app.exec()
