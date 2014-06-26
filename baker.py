# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Anime():
    episodes = []
    params = {'': False}

    def __init__(self, path):
        self.folder = path
        content = os.listdir(self.folder)
        for item in content:
            if '.mkv' in item:
                self.episodes.append(item)
        self.episodes.sort()
        self.quantity = len(self.episodes)

    def n(self):
        return self.quantity

    def list(self):
        return self.episodes

    def episode(self, n):
        print('episode :', self.episodes[n])
        return self.episodes[n][:-4]


class Converter():
    need_convert = False
    audio = [False, 'path', 'params']
    subs = [False, 'path', 'params']

    def x264(self, folder, file):
        preset = 'x264 --tune animation --profile high --level 4.2 --crf 17 --fps 23.976 --preset fast -o "'
        query = preset + file + '.x264" "' + folder + '\\' + file + '.mkv"'
        print(query)
        os.system(query)

    def mkvmerge(self, folder, file):
        if not os.path.exists(folder + '\\8bit'):
            os.makedirs(folder + '\\8bit')
        v = '"' + folder + '\\' + file + '.mkv" '
        v8 = '"' + file + '.x264" '
        a = '--forced-track "0:yes" --default-track "0:yes" "' + self.audio[1] + '\\' + file + '.mka" '
        s = '--forced-track "0:yes" --default-track "0:yes" "' + self.subs[1] + '\\' + file + '.ass" '
        query = 'mkvmerge -o "' + folder + '\\8bit\\' + file + '.mkv" '  # TODO: прибавить исходный файл
        if self.need_convert:
            query += (v8 + '-D ')
        query += v
        if self.audio[0]:
            query += a
        if self.subs[0]:
            query += s
        print(query)
        #os.system(query)
        process = QtCore.QProcess(MainWindow)
        process.startDetached(query)

    def convert(self, start, end):
        for i in range(start, end+1):
            if self.need_convert:
                self.x264(anime.folder, anime.episode(i-1))
            self.mkvmerge(anime.folder, anime.episode(i-1))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(351, 290)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.infoBox = QtGui.QGroupBox(self.centralwidget)
        self.infoBox.setGeometry(QtCore.QRect(10, 10, 331, 81))
        self.infoBox.setObjectName(_fromUtf8("infoBox"))
        self.layoutWidget = QtGui.QWidget(self.infoBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 311, 59))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.pathLabel = QtGui.QLabel(self.layoutWidget)
        self.pathLabel.setObjectName(_fromUtf8("pathLabel"))
        self.horizontalLayout_4.addWidget(self.pathLabel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        self.numLabel = QtGui.QLabel(self.layoutWidget)
        self.numLabel.setObjectName(_fromUtf8("numLabel"))
        self.horizontalLayout_5.addWidget(self.numLabel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_6.addWidget(self.label_8)
        self.bitLabel = QtGui.QLabel(self.layoutWidget)
        self.bitLabel.setObjectName(_fromUtf8("bitLabel"))
        self.horizontalLayout_6.addWidget(self.bitLabel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.layoutWidget1 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 180, 331, 73))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.resetButton = QtGui.QPushButton(self.layoutWidget1)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.horizontalLayout_2.addWidget(self.resetButton)
        self.runButton = QtGui.QPushButton(self.layoutWidget1)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.horizontalLayout_2.addWidget(self.runButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        '''self.progressBar = QtGui.QProgressBar(self.layoutWidget1)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_3.addWidget(self.progressBar)'''
        self.layoutWidget2 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 100, 331, 81))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.convertBox = QtGui.QCheckBox(self.layoutWidget2)
        self.convertBox.setObjectName(_fromUtf8("convertBox"))
        self.verticalLayout.addWidget(self.convertBox)
        self.audioBox = QtGui.QCheckBox(self.layoutWidget2)
        self.audioBox.setObjectName(_fromUtf8("audioBox"))
        self.verticalLayout.addWidget(self.audioBox)
        self.subBox = QtGui.QCheckBox(self.layoutWidget2)
        self.subBox.setObjectName(_fromUtf8("subBox"))
        self.verticalLayout.addWidget(self.subBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.layoutWidget2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.start = QtGui.QSpinBox(self.layoutWidget2)
        self.start.setToolTip(_fromUtf8(""))
        self.start.setStatusTip(_fromUtf8(""))
        self.start.setWhatsThis(_fromUtf8(""))
        self.start.setObjectName(_fromUtf8("start"))
        self.start.setMinimum(1)
        self.horizontalLayout.addWidget(self.start)
        self.label_2 = QtGui.QLabel(self.layoutWidget2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.end = QtGui.QSpinBox(self.layoutWidget2)
        self.end.setToolTip(_fromUtf8(""))
        self.end.setStatusTip(_fromUtf8(""))
        self.end.setWhatsThis(_fromUtf8(""))
        self.end.setObjectName(_fromUtf8("end"))
        self.end.setMinimum(1)
        self.horizontalLayout.addWidget(self.end)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 351, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionChoose = QtGui.QAction(MainWindow, triggered=self.open)
        self.actionChoose.setObjectName(_fromUtf8("actionChoose"))
        self.actionCheck = QtGui.QAction(MainWindow)
        self.actionCheck.setObjectName(_fromUtf8("actionCheck"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menu.addAction(self.actionChoose)
        self.menu.addAction(self.actionCheck)
        self.menu.addAction(self.actionAbout)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.resetButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda l=False: self.convertBox.setChecked(l))
        QtCore.QObject.connect(self.resetButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda l=False: self.audioBox.setChecked(l))
        QtCore.QObject.connect(self.resetButton, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda l=False: self.subBox.setChecked(l))
        QtCore.QObject.connect(self.convertBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), lambda l: self.set_convert(l))
        QtCore.QObject.connect(self.audioBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), lambda l: self.set_audio(l))
        QtCore.QObject.connect(self.subBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), lambda l: self.set_subs(l))
        QtCore.QObject.connect(self.runButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.bake)
        QtCore.QObject.connect(self.start, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), lambda l: self.end.setMinimum(l))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Bake My Anime", None))
        self.infoBox.setTitle(_translate("MainWindow", "Anime info", None))
        self.label_3.setText(_translate("MainWindow", "Path:", None))
        self.pathLabel.setText(_translate("MainWindow", "-", None))
        self.label_6.setText(_translate("MainWindow", "Number of episodes found:", None))
        self.numLabel.setText(_translate("MainWindow", "-", None))
        self.label_8.setText(_translate("MainWindow", "Bit depth:", None))
        self.bitLabel.setText(_translate("MainWindow", "-", None))
        self.runButton.setText(_translate("MainWindow", "Bake!", None))
        self.resetButton.setText(_translate("MainWindow", "Reset", None))
        #self.progressBar.setFormat(_translate("MainWindow", "%p %", None))
        self.convertBox.setText(_translate("MainWindow", "Convert 10bit -> 8 bit", None))
        self.audioBox.setText(_translate("MainWindow", "Include separate audio", None))
        self.subBox.setText(_translate("MainWindow", "Include separate subtitles", None))
        self.label.setText(_translate("MainWindow", "Process with episodes from", None))
        self.label_2.setText(_translate("MainWindow", "to", None))
        self.menu.setTitle(_translate("MainWindow", "More", None))
        self.actionChoose.setText(_translate("MainWindow", "Choose Anime folder", None))
        self.actionCheck.setText(_translate("MainWindow", "Check tools", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))

    def open(self):
        folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", QtCore.QDir.currentPath())
        global anime, converter
        anime = Anime(folder)
        converter = Converter()
        self.pathLabel.setText(folder)
        self.numLabel.setText(str(anime.n()))
        self.start.setMaximum(anime.n())
        self.end.setMaximum(anime.n())

    def set_convert(self, need):
        converter.need_convert = need

    def set_audio(self, need):
        if need:
            folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", anime.folder)
            if folder != '':
                converter.audio = [True, folder, '']
                print(converter.audio)
            else:
                print('No folder!')
                self.audioBox.setChecked(False)
        else:
            converter.audio = [False, '', '']

    def set_subs(self, need):
        if need:
            folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", anime.folder)
            if folder != '':
                converter.subs = [True, folder, '']
            else:
                print('No folder!')
                self.subBox.setChecked(False)
        else:
            converter.subs = [False, '', '']

    def bake(self):
        print('Bake!')
        converter.convert(self.start.value(), self.end.value())
        print('Done!')

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.open()
    MainWindow.show()
    sys.exit(app.exec_())
