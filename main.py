import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog,
    QLineEdit, QMessageBox
)

class PyToExeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py to EXE Converter")
        self.setGeometry(200, 200, 420, 220)

        self.layout = QVBoxLayout()

        self.label = QLabel("Select Python file (.py)")
        self.layout.addWidget(self.label)

        self.path_input = QLineEdit()
        self.layout.addWidget(self.path_input)

        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse_file)
        self.layout.addWidget(self.btn_browse)

        self.btn_convert = QPushButton("Convert to EXE")
        self.btn_convert.clicked.connect(self.convert_to_exe)
        self.layout.addWidget(self.btn_convert)

        self.setLayout(self.layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Python File", "", "Python Files (*.py)"
        )
        if file_path:
            self.path_input.setText(file_path)

    def convert_to_exe(self):
        py_file = self.path_input.text().strip()

        if not py_file.endswith(".py"):
            QMessageBox.critical(self, "Error", "Invalid .py file")
            return

        if not os.path.exists(py_file):
            QMessageBox.critical(self, "Error", "File not found")
            return

        try:
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--distpath=output/dist",
                "--workpath=output/build",
                "--specpath=output",
                py_file
            ]

            subprocess.run(cmd, check=True)

            with open("logs/build.log", "a") as f:
                f.write(f"Built: {py_file}\n")

            QMessageBox.information(self, "Success", "Build done! Check output/dist")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyToExeApp()
    window.show()
    sys.exit(app.exec_())
