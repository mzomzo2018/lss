# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowONdmrI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(862, 665)
        icon = QIcon()
        icon.addFile(u"logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionAbout_project = QAction(MainWindow)
        self.actionAbout_project.setObjectName(u"actionAbout_project")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.webEngineView = QWebEngineView(self.frame)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.webEngineView.setStyleSheet(u"QWebEngineView\n"
"{\n"
"	border-radius: 5px\n"
"}")
        self.webEngineView.setUrl(QUrl(u"http://127.0.0.1:8050/html/index.html"))

        self.gridLayout.addWidget(self.webEngineView, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.statusProgress = QProgressBar(self.centralwidget)
        self.statusProgress.setObjectName(u"statusProgress")
        self.statusProgress.setValue(24)

        self.verticalLayout.addWidget(self.statusProgress)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 862, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMinimumSize(QSize(0, 0))
        icon1 = QIcon()
        icon1.addFile(u"icons8-info-24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu.setIcon(icon1)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionAbout_project)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sham project - Laptop support system", None))
        self.actionAbout_project.setText(QCoreApplication.translate("MainWindow", u"About project", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

