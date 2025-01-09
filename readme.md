# Laptop Support System

## Project Structure

### Python Files

- `mainwindow.py`: Main application window implementation. Contains server setup, WMI queries for system information, and handles communication between UI and backend. Includes the MainWindow class that sets up the UI and manages web view interactions.

- `Laptop.py`: Defines the Laptop class that encapsulates laptop specifications including manufacturer, model, CPU, GPU, RAM and storage details. Uses Python properties for controlled access to attributes.

- `Driver.py`: Implements the Driver dataclass for managing driver information including name, version and release date.

- `UserDetails.py`: Contains the UserDetails dataclass for storing user information like username and email, with validation and formatting logic.

- `ui_mainwindow.py`: Auto-generated Python file from ui_mainwindow.ui containing the UI class definition.

### Qt UI Files

- `ui_mainwindow.ui`: Qt Designer UI file defining the main application window layout and widgets.

- `about.ui`: Qt Designer UI file for the about dialog window.

### HTML Files

- `html/index.htm`: Main page displaying system specifications retrieved from WMI queries.

- `html/contribute.html`: Form page for users to contribute laptop information, with autofill capabilities from system data.
  
- `html/drivers.html`: Displays drivers to be installed using automatic or manual installation.

### Static Files

- `images/`: Directory containing image assets used in the UI
- `fonts/`: Directory containing custom fonts
- `icons/`: Directory containing application icons

## Key Features

- Real-time system information detection using WMI
- Web-based UI using Qt WebEngine
- Local HTTP server for API endpoints
- Automated form filling with detected system specs
- Clean separation between UI and business logic
