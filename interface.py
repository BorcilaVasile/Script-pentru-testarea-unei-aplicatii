import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QScrollArea, QTextEdit, QMainWindow
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame

class ShowTextWindow(QMainWindow):
    def __init__(self, text,title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 600, 400)

        text_edit = QTextEdit()
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)

        self.setCentralWidget(text_edit)

class ClickableLabel(QLabel):
    def __init__(self, text_to_display,title, parent=None):
        super().__init__(parent)
        self.setText("Click me to open a new window")
        self.setStyleSheet("color: blue; text-decoration: underline;")
        self.text_to_display = text_to_display
        self.title=title

    def mousePressEvent(self, event):
        self.open_new_window(self.text_to_display, self.title)

    def open_new_window(self, string,title):
        self.new_window =ShowTextWindow(string,title)
        self.new_window.show()


class Menu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_execution_time = parent.show_execution_time
        self.show_erros = parent.show_erros
        self.show_files = parent.show_files
        self.show_returned_value = parent.show_returned_value
        self.show_result = parent.show_result
        self.show_signal = parent.show_signal
        self.show_system_calls = parent.show_system_calls
        self.show_library_calls = parent.show_library_calls

        self.initUI()

    def initUI(self):
        self.setGeometry(850, 50, 200, 500)
        self.setWindowTitle("Menu")
        self.layout = QVBoxLayout(self)

        # Create header widget and layout
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setSpacing(0)
        self.header_widget.setLayout(self.header_layout)

        # Create scroll area and widget for content
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        #create succes area 
        self.succes_widget = QWidget()
        self.succes_layout = QVBoxLayout(self.succes_widget)
        self.succes_widget.setLayout(self.succes_layout)

        # Add header and scroll area to the main layout
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.succes_widget)

        self.setStyleSheet("background-color: white;")

    def update_layout(self):
        # Clear the existing header layout
        while self.header_layout.count():
            child = self.header_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        #clear the existing succes layout
        while self.succes_layout.count():
            child = self.succes_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        #clear the existing test layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.setStyleSheet("background-color: white;")

        # Create the header row
        self.header_layout.addWidget(QLabel("Test"))
        if self.show_execution_time.isChecked():
            self.header_layout.addWidget(QLabel("Execution Time"))
        if self.show_erros.isChecked():
            self.header_layout.addWidget(QLabel("Errors"))
        if self.show_files.isChecked():
            self.header_layout.addWidget(QLabel("Files"))
        if self.show_returned_value.isChecked():
            self.header_layout.addWidget(QLabel("Returned Value"))
        if self.show_result.isChecked():
            self.header_layout.addWidget(QLabel("Expected result"))
            self.header_layout.addWidget(QLabel("Obtained result"))
        if self.show_signal.isChecked():
            self.header_layout.addWidget(QLabel("Signal"))
        if self.show_system_calls.isChecked():
            self.header_layout.addWidget(QLabel("System Calls"))
        if self.show_library_calls.isChecked():
            self.header_layout.addWidget(QLabel("Library Calls"))
        self.header_layout.addWidget(QLabel("Result"))

        # Iterate over each test file
        for i in range(MyWidget.number_of_tests):
            try:
                with open("test" + str(i+1) + ".txt", "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                lines = ["File not found"]
            except Exception as e:
                lines = [f"Error: {e}"]

            rowlayout = QHBoxLayout()
            rowlayout.setSpacing(0)
            rowlayout.setSizeConstraint(QHBoxLayout.SetFixedSize)

            result = lines[-1].strip() if len(lines) > 4 else "N/A"

            test_label = QLabel("Test " + str(i+1))
            test_label.setFixedHeight(30)
            if "Passed" in result:
                test_label.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
            else:
                test_label.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
            rowlayout.addWidget(test_label)

            if self.show_execution_time.isChecked():
                execution_time = lines[0].strip() if len(lines) > 0 else "N/A"
                label = QLabel(execution_time)
                label.setFixedHeight(30)
                if "Passed" in result:
                    label.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    label.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(label)

            if self.show_erros.isChecked():
                errors = lines[1].strip() if len(lines) > 1 else "N/A"
                if errors == "No errors":
                    label = QLabel(errors)
                else:
                    label = ClickableLabel(errors,"Errors")
                    label.setText("See errors")
                label.setFixedHeight(30)
                if "Passed" in result:
                    label.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    label.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                label.wordWrap()
                rowlayout.addWidget(label)

            if self.show_files.isChecked():
                files = lines[2].strip() if len(lines) > 2 else "N/A"
                if files == "No files created":
                    label = QLabel(files)
                else:
                    label = ClickableLabel(files,"Created files")
                    label.setText("See files")
                label.setFixedHeight(30)
                if "Passed" in result:
                    label.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    label.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(label)

            if self.show_returned_value.isChecked():
                returned_value = lines[3].strip() if len(lines) > 3 else "N/A"
                label = QLabel(returned_value)
                label.setFixedHeight(30)
                if "Passed" in result:
                    label.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    label.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(label)

            if self.show_result.isChecked():
                expected_result = lines[4].strip() if len(lines) > 4 else "N/A"
                obtained_result = lines[5].strip() if len(lines) > 5 else "N/A"
                label1 = QLabel(expected_result)
                label1.setFixedHeight(30)
                if "Passed" in result:
                    label1.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    label1.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(label1)
                label2 = QLabel(obtained_result)
                label2.setFixedHeight(30)
                if "Passed" in result:
                    label2.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    label2.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(label2)

            if self.show_signal.isChecked():
                signal_text=lines[6].strip() if len(lines) > 6 else "N/A"

                found_system_calls = None
                for index, line in enumerate(lines):
                    if "System calls:" in line:
                        found_system_calls = index
                        break
                if found_system_calls is not None:
                    signal_text = "".join(lines[6:found_system_calls])

                signal=ClickableLabel(signal_text,"Signal")
                signal.setText("See signal")
                signal.setFixedHeight(30)
                if "Passed" in result:
                    signal.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    signal.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(signal)


            if self.show_system_calls.isChecked():
                system_calls_text=lines[7].strip() if len(lines) > 7 else "N/A"

                found_system_calls = None
                for index, line in enumerate(lines):
                    if "System calls:" in line:
                        found_system_calls = index
                        break

                found_library_calls = None
                for index, line in enumerate(lines):
                    if "Library calls:" in line:
                        found_library_calls = index
                        break
                system_calls_text = "".join(lines[found_system_calls:found_library_calls])

                system_calls=ClickableLabel(system_calls_text,"System Calls")
                system_calls.setText("See system calls")
                system_calls.setFixedHeight(30)
                if "Passed" in result:
                    system_calls.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    system_calls.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(system_calls)
            if self.show_library_calls.isChecked():
                library_calls_text=lines[8].strip() if len(lines) > 8 else "N/A"

                found_library_calls = None
                for index, line in enumerate(lines):
                    if "Library calls:" in line:
                        found_library_calls = index
                        break
                if found_library_calls is not None:
                    library_calls_text = "".join(lines[found_library_calls:len(lines)-1])

                library_calls=ClickableLabel(library_calls_text,"Library Calls")
                library_calls.setText("See library calls")
                library_calls.setFixedHeight(30)
                if "Passed" in result:
                    library_calls.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
                else:
                    library_calls.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
                rowlayout.addWidget(library_calls)
            
            result_label = QLabel(result)
            result_label.setFixedHeight(30)
            if "Passed" in result:
                result_label.setStyleSheet("background-color: #c6efce; border: 1px solid black;")
            else:
                result_label.setStyleSheet("background-color: #ffcccb; border: 1px solid black;")
            rowlayout.addWidget(result_label)

            self.scroll_layout.addLayout(rowlayout)

        try:
            with open('succes.txt', 'r') as file:
                succes_rate = file.readline().strip()
        except FileNotFoundError:
            succes_rate = None

        if succes_rate:
            self.succes_layout.addWidget(QLabel(succes_rate))
        else:
            self.succes_layout.addWidget(QLabel("No tests have been run yet"))

        self.show()

class MyWidget(QWidget):
    number_of_tests = 0
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle("Framework")

        # Layout-ul principal vertical
        self.mainLayout = QVBoxLayout(self)

        # Input pentru calea aplicației
        self.path = QLineEdit(self)
        self.path.setPlaceholderText("Enter the path to the application")
        self.path.setFixedSize(self.width() - 100, 40)
        self.mainLayout.addWidget(self.path)

        self.options_and_menu_layout = QHBoxLayout()
        # Checkbox-uri pentru diferite opțiuni
        options_layout = QVBoxLayout()
        options_layout.setSpacing(5)
        self.show_execution_time = QCheckBox("Show execution time")
        self.show_erros = QCheckBox("Show errors")
        self.show_files = QCheckBox("Show created files")
        self.show_returned_value = QCheckBox("Show returned value")
        self.show_result = QCheckBox("Show result")
        self.show_signal = QCheckBox("Show signal")
        self.show_system_calls = QCheckBox("Show system calls")
        self.show_library_calls = QCheckBox("Show library calls")

        self.show_execution_time.setFixedSize(200, 20)
        self.show_erros.setFixedSize(200, 20)
        self.show_files.setFixedSize(200, 20)
        self.show_returned_value.setFixedSize(200, 20)
        self.show_result.setFixedSize(200, 20)
        self.show_signal.setFixedSize(200, 20)
        self.show_system_calls.setFixedSize(200, 20)
        self.show_library_calls.setFixedSize(200, 20)

        self.show_execution_time.stateChanged.connect(self.checkbox_state_changed)
        self.show_erros.stateChanged.connect(self.checkbox_state_changed)
        self.show_files.stateChanged.connect(self.checkbox_state_changed)
        self.show_returned_value.stateChanged.connect(self.checkbox_state_changed)
        self.show_result.stateChanged.connect(self.checkbox_state_changed)
        self.show_signal.stateChanged.connect(self.checkbox_state_changed)
        self.show_system_calls.stateChanged.connect(self.checkbox_state_changed)
        self.show_library_calls.stateChanged.connect(self.checkbox_state_changed)

        options_layout.addWidget(self.show_execution_time)
        options_layout.addWidget(self.show_erros)
        options_layout.addWidget(self.show_files)
        options_layout.addWidget(self.show_returned_value)
        options_layout.addWidget(self.show_result)
        options_layout.addWidget(self.show_signal)
        options_layout.addWidget(self.show_system_calls)
        options_layout.addWidget(self.show_library_calls)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        options_layout.addItem(spacer)
        self.mainLayout.addLayout(options_layout)

        # Butoanele pentru adăugare test, start test și cancel
        buttons_layout = QHBoxLayout()
        self.buttonAddTest = QPushButton("Add Test", self)
        self.buttonStart = QPushButton("Start Test", self)
        self.buttonCancel = QPushButton("Cancel", self)

        self.buttonAddTest.setFixedSize(100, 40)
        self.buttonStart.setFixedSize(100, 40)
        self.buttonCancel.setFixedSize(100, 40)

        self.buttonAddTest.clicked.connect(self.buttonAddTest_clicked)
        self.buttonStart.clicked.connect(self.buttonStart_clicked)
        self.buttonCancel.clicked.connect(self.buttonCancel_clicked)

        buttons_layout.addWidget(self.buttonAddTest)
        buttons_layout.addWidget(self.buttonStart)
        buttons_layout.addWidget(self.buttonCancel)

        self.options_and_menu_layout.addLayout(options_layout)
        self.menuLayout = QVBoxLayout()
        self.options_and_menu_layout.addLayout(self.menuLayout) 
        self.mainLayout.addLayout(self.options_and_menu_layout)
        self.mainLayout.addLayout(buttons_layout)

        self.create_menu()  # Inițializăm meniul la început

    def checkbox_state_changed(self):
        self.update_menu()  # Actualizăm meniul când se schimbă starea unui checkbox

    def create_menu(self):
        self.menu = Menu(self)
        self.menu.update_layout()
        self.menuLayout.addWidget(self.menu)

    def update_menu(self):
        self.menu.update_layout()

    def buttonStart_clicked(self):
        selected_options = []

        if self.show_execution_time.isChecked():
            selected_options.append("1")
        if self.show_erros.isChecked():
            selected_options.append("2")
        if self.show_files.isChecked():
            selected_options.append("3")
        if self.show_returned_value.isChecked():
            selected_options.append("4")
        if self.show_result.isChecked():
            selected_options.append("5")
        if self.show_signal.isChecked():
            selected_options.append("6")
        if self.show_system_calls.isChecked():
            selected_options.append("7")
        if self.show_library_calls.isChecked():
            selected_options.append("8")

        choice = "".join(selected_options) 
        if choice == "":
            choice = "9"

        if self.path.text() == "":
            return
        else:
            with open("configuration_file.txt", "w") as file:
                file.write("Path to application: "+self.path.text()+"\n")
                file.write("Arguments: argumente.txt\n")
                file.write("Input files: ")
                for i in range(MyWidget.number_of_tests):
                    file.write("input"+str(i+1)+".txt ")
                file.write("\n")
                file.write("Expected output: expected_output.txt\n")
        process = subprocess.Popen(['bash', 'Framework2.sh', choice], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.update_menu()

    def buttonCancel_clicked(self):
        if os.path.exists("configuration_file.txt"):
            os.remove("configuration_file.txt")
        if os.path.exists("succes.txt"):
            os.remove("succes.txt")
        if os.path.exists("argumente.txt"):
            os.remove("argumente.txt")
        if os.path.exists("expected_output.txt"):
            os.remove("expected_output.txt")
        for i in range(MyWidget.number_of_tests):
            if os.path.exists("input"+str(i+1)+".txt"):
                os.remove("input"+str(i+1)+".txt")
        for i in range(MyWidget.number_of_tests):
            if os.path.exists("test"+str(i+1)+".txt"):
                os.remove("test"+str(i+1)+".txt")
        if os.path.exists("strace_output.txt"):
            os.remove("strace_output.txt")
        if os.path.exists("ltrace_output.txt"):
            os.remove("ltrace_output.txt")
        if os.path.exists("strace_signals.txt"):
            os.remove("strace_signals.txt")
        if os.path.exists("errors.txt"):
            os.remove("errors.txt")
        self.close()

    def buttonAddTest_clicked(self):
        self.new_window = TestWindow()
        self.new_window.show()


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.number_of_tests = MyWidget.number_of_tests

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Test Window")

        layout = QVBoxLayout()

        self.labelArguments = QLineEdit(self)
        self.labelArguments.setPlaceholderText("Enter the arguments")
        layout.addWidget(self.labelArguments)

        self.labelInput = QLineEdit(self)
        self.labelInput.setPlaceholderText("Enter the input")
        layout.addWidget(self.labelInput)

        self.labelOutput = QLineEdit(self)
        self.labelOutput.setPlaceholderText("Enter the output")
        layout.addWidget(self.labelOutput)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveButton_clicked)
        layout.addWidget(self.saveButton)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)
        layout.addWidget(self.cancelButton)

        self.setLayout(layout)

    def saveButton_clicked(self):
        MyWidget.number_of_tests += 1
        arguments = self.labelArguments.text()
        input = self.labelInput.text()
        output = self.labelOutput.text()
        with open("argumente.txt", "a") as arg_file:
            arg_file.write(arguments + "\n")
        with open("expected_output.txt", "a") as output_file:
            output_file.write(output + "\n")
        name_of_file="input"+str(MyWidget.number_of_tests)+".txt"
        with open(name_of_file, "a") as input_file:
            input_file.write(input + "\n")
        self.close()


def window():
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
