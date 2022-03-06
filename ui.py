import datetime

from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from note import Note


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.note_editor = NoteEditor(self)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.note_editor)

        self.setVisible(True)
        self.setWindowTitle("Diary")


class NoteEditor(QtWidgets.QWidget):
    send_note = pyqtSignal(Note)

    def __init__(self, parent=None):
        super(NoteEditor, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setPlaceholderText("Write please")
        self.layout().addWidget(self.text_edit)


        options = QtWidgets.QWidget()
        options.setLayout(QtWidgets.QHBoxLayout())

        self.scope = QtWidgets.QSpinBox()
        self.scope.setMaximum(10)
        self.scope.setMinimum(0)
        options.layout().addWidget(self.scope)

        self.change_type = QtWidgets.QComboBox()
        #TODO edit to load types from db
        self.change_type.addItems(["Daily", "Monthly"])
        options.layout().addWidget(self.change_type)

        self.layout().addWidget(options)

        self.save_button = QtWidgets.QPushButton(self)
        self.save_button.setText("Save")
        self.save_button.clicked.connect(
            lambda: self.send_note.emit(self.get_note()))
        self.layout().addWidget(self.save_button)

    def get_note(self) -> Note:
        return Note(self.text_edit.toPlainText(),
                    self.change_type.currentText(),
                    datetime.datetime.now(),
                    int(self.scope.text()))

class NotesViewer(QtWidgets.QWidget):
    start_update = pyqtSignal()

    def __init__(self, parent):
        super(NotesViewer, self).__init__(parent)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.notes_list = QtWidgets.QListWidget()
        self.layout().addWidget(self.notes_list)

        self.update_button = QtWidgets.QPushButton("Update")
        self.update_button.clicked.connect(lambda: self.start_update.emit())
        self.layout().addWidget(self.update_button)

    def update_notes(self, notes: list[Note]):
        self.notes_list.clear()
        for note in notes:
            self.notes_list.addItem(QtWidgets.QListWidgetItem(
                f"{note.type}: {note.text} from {note.date} with scope {note.scope}"
            ))
