import decimal
import sqlite3
import sys
import threading
import json
import os
import mimetypes
import win32com.client
from http.server import HTTPServer, BaseHTTPRequestHandler

import wmi
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtNetwork import QLocalServer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtWebEngineCore import QWebEngineSettings

from Driver import Driver
from UserDetails import UserDetails
from Laptop import Laptop

from ui_mainwindow import Ui_MainWindow


def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, status_code, data=None, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        if data:
            if content_type == 'application/json':
                self.wfile.write(json.dumps(data).encode())
            else:
                self.wfile.write(data)

    def do_OPTIONS(self):
        self._send_response(200)

    def do_GET(self):
        if self.path == '/optimize':
            try:
                os.system('sfc /scannow')
                os.system('cleanmgr /sagerun:1')
                os.system('defrag C: /O')
                os.system('del /s /q %temp%\\*.*')
                os.system('net stop wuauserv')
                os.system('net stop cryptSvc')
                os.system('net stop bits')
                os.system('net stop msiserver')
                os.system('ipconfig /flushdns')
                os.system('wsreset')
                
                self._send_response(200, {'message': 'Optimization completed successfully'})
            except Exception as e:
                self._send_response(500, {'error': str(e)})
        elif self.path == '/detectDrivers':
            try:
                import wmi
                w = wmi.WMI()
                installed_drivers = w.Win32_PnPSignedDriver()

                conn = sqlite3.connect('drivers.db')
                cursor = conn.cursor()

                available_drivers = []
                for installed in installed_drivers:
                    cursor.execute("""
                        SELECT id, name, version, release_date FROM drivers 
                        WHERE device_class = ? AND version > ?
                    """, (installed.DeviceClass, installed.DriverVersion))
                    
                    newer_drivers = cursor.fetchall()
                    for newer in newer_drivers:
                        driver = Driver()
                        driver.name = newer[1]
                        driver.version = newer[2]
                        driver.release_date = newer[3]
                        available_drivers.append({
                            'id': newer[0],
                            'name': driver.get_name(),
                            'version': driver.get_version(),
                            'release_date': driver.get_release_date()
                        })

                conn.close()
                self._send_response(200, {
                    'found': len(available_drivers) > 0,
                    'drivers': available_drivers
                })
            except Exception as e:
                self._send_response(500, {'error': str(e)})
        elif self.path == '/installationProgress':
            if self.installation_in_progress:
                try:
                    total_drivers = len(self.selected_drivers)

                    progress_per_driver = 100 / total_drivers
                    current_driver_index = int(self.current_progress / progress_per_driver)
                    
                    if current_driver_index < total_drivers:
                        driver = self.selected_drivers[current_driver_index]
                        driver_path = os.path.join('drivers', f"{driver['name']}.exe")
                        
                        if os.path.exists(driver_path):
                            os.system(f'"{driver_path}" /S')
                            self.current_progress = (current_driver_index + 1) * progress_per_driver
                    
                    if self.current_progress >= 100:
                        self.installation_in_progress = False
                        self.current_progress = 100
                        self.selected_drivers = []
                    
                    self._send_response(200, {
                        'progress': self.current_progress,
                        'currentDriver': current_driver_index + 1,
                        'totalDrivers': total_drivers
                    })
                except Exception as e:
                    self.installation_in_progress = False
                    self._send_response(500, {'error': str(e)})
            else:
                self._send_response(200, {'progress': 0})
        else:
            try:
                file_path = os.path.join(os.path.dirname(__file__), self.path.lstrip('/'))
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    mime_type, _ = mimetypes.guess_type(file_path)
                    if mime_type is None:
                        mime_type = 'application/octet-stream'
                        
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    self._send_response(200, content, mime_type)
                else:
                    self._send_response(404)
            except Exception:
                self._send_response(500)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = json.loads(self.rfile.read(content_length)) if content_length > 0 else {}

        if self.path == '/registerLaptop':
            try:
                conn = sqlite3.connect('laptops.db')
                cursor = conn.cursor()

                cursor.execute('''CREATE TABLE IF NOT EXISTS laptops (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    manufacturer TEXT,
                    model_family TEXT, 
                    model TEXT,
                    production_date TEXT,
                    cpu TEXT,
                    integrated_gpu TEXT,
                    dedicated_gpu TEXT,
                    ram TEXT,
                    storage TEXT,
                    windows_version TEXT,
                    build_version TEXT,
                    username TEXT,
                    email TEXT
                )''')

                user = UserDetails()
                user.set_username(post_data.get('username', ''))
                user.set_email(post_data.get('email', ''))

                laptop = Laptop()
                laptop.model_family = post_data.get('modelFamily')
                laptop.model = post_data.get('model')
                laptop.cpu = post_data.get('cpu')
                laptop.integrated_gpu = post_data.get('integratedGpu')
                laptop.dedicated_gpu = post_data.get('dedicatedGpu')
                laptop.ram = post_data.get('ram')
                laptop.storage = post_data.get('storage')

                cursor.execute('''INSERT INTO laptops (
                    manufacturer, model_family, model, production_date,
                    cpu, integrated_gpu, dedicated_gpu, ram, storage,
                    windows_version, build_version, username, email
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    post_data.get('manufacturer'),
                    laptop.model_family,
                    laptop.model,
                    post_data.get('productionDate'),
                    laptop.cpu,
                    laptop.integrated_gpu,
                    laptop.dedicated_gpu,
                    laptop.ram,
                    laptop.storage,
                    post_data.get('windowsVersion'),
                    post_data.get('buildVersion'),
                    user.get_username(),
                    user.get_email()
                ))

                conn.commit()
                conn.close()
                self._send_response(200, {'message': 'Laptop registered successfully'})
            except Exception as e:
                self._send_response(500, {'error': str(e)})
            self._send_response(200)
        elif self.path == '/prepareInstallation':
            self.selected_drivers = post_data.get('drivers', [])
            self._send_response(200)
        else:
            self._send_response(404)


def create_server():
    server = HTTPServer(('127.0.0.1', 8050), RequestHandler)
    server.serve_forever()


def start_server():
    server = QLocalServer()
    server.listen("LSS_Server")
    http_thread = threading.Thread(target=create_server, daemon=True)
    http_thread.start()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        start_server()
        self.ui.setupUi(self)
        self.ui.webEngineView.loadProgress.connect(self.load_progress_handle)
        self.ui.actionAbout_project.triggered.connect(self.about_menu_button_clicked)
        self.ui.webEngineView.loadFinished.connect(self.load_finished)

    def load_finished(self):
        url = self.ui.webEngineView.page().url().toString()
        wmi_object = wmi.WMI()
        win32_cs_object = wmi_object.Win32_ComputerSystem()[0]
        win32_processor_object = wmi_object.Win32_Processor()[0]
        win32_gpu_object = wmi_object.Win32_VideoController()
        win32_memory_object = wmi_object.Win32_PhysicalMemory()
        win32_os_object = wmi_object.Win32_OperatingSystem()[0]
        win32_storage_object = wmi.WMI(namespace="root\\Microsoft\\Windows\\Storage").MSFT_PhysicalDisk()
        def detect_media_type(index: int) -> str:
            if index == 4:
                return "SSD"
            elif index == 3:
                return "HDD"
        dedicated_gpu = '-'
        if len(win32_gpu_object) > 1:
            dedicated_gpu = f"{win32_gpu_object[1].Caption} "
            gpu_ram = format_size(int(str(win32_gpu_object[1])[str(win32_gpu_object[1]).index("AdapterRAM =") + 12:str(win32_gpu_object[1]).index("Availability") - 3]))
            dedicated_gpu += gpu_ram

        integrated_gpu_ram = format_size(int(win32_gpu_object[0].AdapterRAM))
        ram_sizes = [format_size(int(x.Capacity)) for x in win32_memory_object]
        storage_sizes = [f"{format_size(int(x.Size))} {detect_media_type(int(x.MediaType))}"
                       for x in win32_storage_object]

        laptop = Laptop()
        laptop.manufacturer = str(win32_cs_object.Manufacturer).title()
        laptop.model_family = " ".join(str(win32_cs_object.SystemFamily).split()[:-1:1])
        laptop.model = str(win32_cs_object.Model)
        laptop.cpu = f"{win32_processor_object.Name} {round(win32_processor_object.CurrentClockSpeed / 1000, 2)} GHz {win32_processor_object.NumberOfCores} cores"
        laptop.integrated_gpu = f"{win32_gpu_object[0].Caption} {integrated_gpu_ram}"
        laptop.dedicated_gpu = dedicated_gpu
        laptop.ram = f"{' + '.join(ram_sizes)} {win32_memory_object[0].ConfiguredClockSpeed} MHz"
        laptop.storage = ' + '.join(storage_sizes)

        if "index.htm" in url:
            pc_specs = {
                'manufacturer': laptop.manufacturer,
                'modelFamily': laptop.model_family,
                'model': laptop.model,
                'productionDate': '-',
                'cpu': laptop.cpu,
                'integratedGpu': laptop.integrated_gpu,
                'dedicatedGpu': laptop.dedicated_gpu,
                'ram': laptop.ram,
                'storage': laptop.storage,
                'windowsVersion': win32_os_object.Caption,
                'buildVersion': (f"{win32_os_object.BuildNumber} "
                               f"{win32_os_object.OSArchitecture}")
            }

            self.ui.webEngineView.page().runJavaScript(f"updatePCSpecs({pc_specs});")
            
        elif "contribute.html" in url:
            laptop_info = {
                'manufacturer': laptop.manufacturer,
                'modelFamily': laptop.model_family,
                'model': laptop.model,
                'productionDate': '-',
                'cpu': laptop.cpu,
                'gpu': laptop.integrated_gpu,
                'dedicatedGpu': laptop.dedicated_gpu,
                'ram': laptop.ram,
                'storage': laptop.storage,
            }
                
            self.ui.webEngineView.page().runJavaScript(f"autofillForm({laptop_info});")

    def load_progress_handle(self, progress: int):
        if progress == 100 or progress == 0:
            self.ui.statusProgress.hide()
        else:
            self.ui.statusProgress.show()
            self.ui.statusProgress.setValue(progress)

    def about_menu_button_clicked(self):
        QUiLoader().load("about.ui", None).exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
