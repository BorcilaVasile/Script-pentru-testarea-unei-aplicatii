import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy


class MyWidget(QWidget):
    number_of_tests = 10
    
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
        self.show_all = QCheckBox("None")

        self.show_execution_time.setFixedSize(200, 20)
        self.show_erros.setFixedSize(200, 20)
        self.show_files.setFixedSize(200, 20)
        self.show_returned_value.setFixedSize(200, 20)
        self.show_result.setFixedSize(200, 20)
        self.show_signal.setFixedSize(200, 20)
        self.show_system_calls.setFixedSize(200, 20)
        self.show_library_calls.setFixedSize(200, 20)
        self.show_all.setFixedSize(200, 20)

        self.show_execution_time.stateChanged.connect(self.checkbox_state_changed)
        self.show_erros.stateChanged.connect(self.checkbox_state_changed)
        self.show_files.stateChanged.connect(self.checkbox_state_changed)
        self.show_returned_value.stateChanged.connect(self.checkbox_state_changed)
        self.show_result.stateChanged.connect(self.checkbox_state_changed)
        self.show_signal.stateChanged.connect(self.checkbox_state_changed)
        self.show_system_calls.stateChanged.connect(self.checkbox_state_changed)
        self.show_library_calls.stateChanged.connect(self.checkbox_state_changed)
        self.show_all.stateChanged.connect(self.checkbox_state_changed)

        options_layout.addWidget(self.show_execution_time)
        options_layout.addWidget(self.show_erros)
        options_layout.addWidget(self.show_files)
        options_layout.addWidget(self.show_returned_value)
        options_layout.addWidget(self.show_result)
        options_layout.addWidget(self.show_signal)
        options_layout.addWidget(self.show_system_calls)
        options_layout.addWidget(self.show_library_calls)
        options_layout.addWidget(self.show_all)

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

        self.update_menu()  # Inițializăm meniul la început

    def checkbox_state_changed(self):
        self.update_menu()  # Actualizăm meniul când se schimbă starea unui checkbox

    def update_menu(self):
        for i in reversed(range(self.menuLayout.count())):
            item = self.menuLayout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            self.menuLayout.removeItem(item)
        self.update()
        self.menuLayout.addWidget(QLabel("Menu"))

        self.menu_info = QHBoxLayout()
        self.menu_info.addWidget(QLabel("Test"))
        if self.show_execution_time.isChecked():
            self.menu_info.addWidget(QLabel("Execution Time"))
        if self.show_erros.isChecked():
            self.menu_info.addWidget(QLabel("Errors"))
        if self.show_files.isChecked():
            self.menu_info.addWidget(QLabel("Created files"))
        if self.show_returned_value.isChecked():
            self.menu_info.addWidget(QLabel("Returned Value"))
        if self.show_result.isChecked():
            self.menu_info.addWidget(QLabel("Expected Output"))
            self.menu_info.addWidget(QLabel("Output"))
        self.menu_info.addWidget(QLabel("Result"))
        self.menuLayout.addLayout(self.menu_info)

        for i in range(1, 5):
            self.test_layout = QHBoxLayout()
            self.labelTest = QLabel(f"Test {i}")
            self.test_layout.addWidget(self.labelTest)
            if self.show_execution_time.isChecked():
                self.labelExecutionTime = QLabel("Execution Time")
                self.test_layout.addWidget(self.labelExecutionTime)
            if self.show_erros.isChecked():
                self.labelErrors = QLabel("Errors")
                self.test_layout.addWidget(self.labelErrors)
            if self.show_files.isChecked():
                self.labelFiles = QLabel("Files")
                self.test_layout.addWidget(self.labelFiles)
            if self.show_returned_value.isChecked():
                self.labelReturnedValue = QLabel("Returned Value")
                self.test_layout.addWidget(self.labelReturnedValue)
            if self.show_result.isChecked():
                self.labelExpectedOutput = QLabel("Expected Output")
                self.labelOutput = QLabel("Output")
                self.test_layout.addWidget(self.labelExpectedOutput)
                self.test_layout.addWidget(self.labelOutput)
            self.labelResult = QLabel("Result")
            self.test_layout.addWidget(self.labelResult)

            self.menuLayout.addLayout(self.test_layout)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.menuLayout.addItem(spacer)

        self.options_and_menu_layout.addLayout(self.menuLayout)
        self.actions()

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
        if self.show_all.isChecked():
            selected_options.append("9")

        choice = "".join(selected_options) 
        process = subprocess.Popen(['bash', 'Framework2.sh', choice], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        MyWidget.update(self)

            

    def buttonCancel_clicked(self):
        self.close()

    def buttonAddTest_clicked(self):
        self.new_window = NewWindow()
        self.new_window.show()


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Test Window")

        layout = QVBoxLayout()

        self.labelArguments = QLineEdit(self)
        self.labelArguments.move(100, 100)
        self.labelArguments.resize(200, 40)
        self.labelArguments.setPlaceholderText("Enter the arguments")
        layout.addWidget(self.labelArguments)

        self.labelInput= QLineEdit(self)
        self.labelInput.move(100, 150)
        self.labelInput.resize(200, 40)
        self.labelInput.setPlaceholderText("Enter the input")
        layout.addWidget(self.labelInput)

        self.labelOutput = QLineEdit(self)
        self.labelOutput.move(100, 200)
        self.labelOutput.resize(200, 40)
        self.labelOutput.setPlaceholderText("Enter the output")
        layout.addWidget(self.labelOutput)

        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.move(100, 250)
        self.saveButton.clicked.connect(self.saveButton_clicked)
        layout.addWidget(self.saveButton)

        self.cancelButton = QPushButton(self)
        self.cancelButton.setText("Cancel")
        self.cancelButton.move(200, 250)
        self.cancelButton.clicked.connect(self.close)
        layout.addWidget(self.cancelButton)


    def saveButton_clicked(self):
        arguments = self.labelArguments.text()
        input = self.labelInput.text()
        output = self.labelOutput.text()
        MyWidget.number_of_tests += 1
        with open("argumente.txt", "a") as arg_file:
            arg_file.write(arguments + "\n")
        with open("expected_output.txt", "a") as output_file:
            output_file.write(output + "\n")
        self.close()


def window():
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
