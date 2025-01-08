# This Python file uses the following encoding: utf-8
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

import wmi
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtNetwork import QLocalServer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtWebEngineCore import QWebEngineSettings

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow

def createServer():
    server = HTTPServer(('127.0.0.1', 8050), SimpleHTTPRequestHandler)
    server.serve_forever()

def startServer():
    server = QLocalServer()
    server.listen("LSS_Server")
    http_thread = threading.Thread(target=createServer, daemon=True)
    http_thread.start()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        startServer()
        self.ui.setupUi(self)
        self.ui.webEngineView.loadProgress.connect(self.loadProgressHandle)
        self.ui.actionAbout_project.triggered.connect(self.aboutMenuButtonClicked)
        self.ui.webEngineView.loadFinished.connect(self.loadFinished)
    def loadFinished(self):
        if "index.htm" in self.ui.webEngineView.page().url().toString():
            wmiObject = wmi.WMI()
            win32CSObject = wmiObject.Win32_ComputerSystem()[0]
            win32ProcessorObject = wmiObject.Win32_Processor()[0]
            win32GPUObject = wmiObject.Win32_VideoController()[0]
            win32MemoryObject = wmiObject.Win32_PhysicalMemory()
            win32OSObject = wmiObject.Win32_OperatingSystem()
            print(win32OSObject)
            win32StorageObject = wmi.WMI(namespace="root\\Microsoft\\Windows\\Storage").MSFT_PhysicalDisk()
            def detectMediaType(index: int) -> str:
                if index == 4:
                    return "SSD"
                elif index == 3:
                    return "HDD"
            self.ui.webEngineView.page().runJavaScript("updatePCSpecs(" + str({ 'manufacturer': str(win32CSObject.Manufacturer).title(), 'modelFamily': " ".join(str(win32CSObject.SystemFamily).split()[:-1:1]), 'model': str(win32CSObject.Model), 'productionDate': '-', 'cpu': win32ProcessorObject.Name, 'gpu': win32GPUObject.Caption, 'ram': ' GB + '.join([str(int(int(x.Capacity) / (1024**3))) for x in win32MemoryObject]) + " GB " + str(win32MemoryObject[0].ConfiguredClockSpeed) + " MHz", 'storage': ' + '.join([str(int(x.Size) / (1024**3)) + " GB " + detectMediaType(int(x.MediaType)) for x in win32StorageObject]), 'windowsVersion': 'Windows 11 Pro', 'buildVersion': '22H2 (19045.3803)'}) + ");")
    def loadProgressHandle(self, progress: int):
        if progress == 100 or progress == 0:
            self.ui.statusProgress.hide()
        else:
            self.ui.statusProgress.show()
            self.ui.statusProgress.setValue(progress)
    def aboutMenuButtonClicked(self):
        QUiLoader().load("about.ui", None).exec()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
