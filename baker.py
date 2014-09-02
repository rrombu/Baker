# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
#TODO: from pymediainfo import MediaInfo
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
    def __init__(self, path):
        self.episodes = []
        self.params = {'': False}
        self.folder = path
        content = os.listdir(self.folder)
        for item in content:
            if '.mkv' in item:
                self.episodes.append(item)
        self.episodes.sort()
        self.quantity = len(self.episodes)

    def n(self):
        return self.quantity

    ### UNDER CONSTRUCTION ###
    '''def bit(self):
        file = self.folder + '\\' + self.episodes[0]
        print(file)
        media_info = MediaInfo.parse("D:\\1.mkv", environment=os.environ)
        for track in media_info.tracks:
            if track.track_type == 'Video':
                print('MediaInfo:', track.bit_rate, track.bit_rate_mode, track.codec)'''
    ###                    ###

    def list(self):
        return self.episodes

    def episode(self, n):
        print('episode :', self.episodes[n])
        return self.episodes[n][:-4]


class Converter(QtCore.QThread):
    update = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    def __init__(self, mw):
        super(Converter, self).__init__()
        self.need_convert = False
        self.audio = [False, 'path', 'params']
        self.subs = [False, 'path', 'params']
        self.first = 0
        self.last = 0
        self.params = '--tune animation --profile high --level 4.2 --crf 17 --fps 23.976 --preset fast'

    def x264(self, folder, file):
        preset = 'x264 {} -o "'.format(self.params)
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
        query = 'mkvmerge -o "' + folder + '\\8bit\\' + file + '.mkv" '
        if self.need_convert:
            query += (v8 + '-D ')
        query += v
        if self.audio[0]:
            query += a
        if self.subs[0]:
            query += s
        print(query)
        os.system(query)

    def run(self):
        for i in range(self.first, self.last+1):
            if self.need_convert:
                self.x264(anime.folder, anime.episode(i-1))
            self.mkvmerge(anime.folder, anime.episode(i-1))
            os.remove(anime.episode(i-1)+'.x264')
            self.update.emit()
        self.finished.emit()

class x264_Dialog(object):
    def setupUi(self, Dialog, value):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(401, 150)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("baker.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 381, 131))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit.setText(value)
        self.verticalLayout.addWidget(self.lineEdit)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "x264 parameters", None))
        self.label.setText(_translate("Dialog", "Below you can see default x264 conversion parameters used in this "
                                                "program. You can change them or add new ones.", None))
        self.label_2.setText(_translate("Dialog", "WARNING! Wrong parameters can break program conversion function!"
                                                  "Restart program to undo any changes.", None))

    def getValues(self):
        return str(self.lineEdit.text())


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(351, 290)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("baker.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        self.progressBar = QtGui.QProgressBar(self.layoutWidget1)
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setMaximum(0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.progressBar.setVisible(False)
        self.verticalLayout_3.addWidget(self.progressBar)
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
        self.start.setObjectName(_fromUtf8("start"))
        self.start.setMinimum(1)
        self.horizontalLayout.addWidget(self.start)
        self.label_2 = QtGui.QLabel(self.layoutWidget2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.end = QtGui.QSpinBox(self.layoutWidget2)
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
        self.actionX264 = QtGui.QAction(MainWindow, triggered=self.x264DIalog)
        self.actionX264.setObjectName(_fromUtf8("actionX264"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menu.addAction(self.actionChoose)
        self.menu.addAction(self.actionCheck)
        self.menu.addAction(self.actionX264)
        self.menu.addAction(self.actionAbout)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.resetButton.clicked.connect(self.abort)
        self.convertBox.toggled.connect(lambda l: self.set_convert(l))
        self.audioBox.toggled.connect(lambda l: self.set_audio(l))
        self.subBox.toggled.connect(lambda l: self.set_subs(l))
        self.runButton.clicked.connect(self.bake)
        self.start.valueChanged.connect(lambda l: self.end.setMinimum(l))
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
        self.convertBox.setText(_translate("MainWindow", "Convert 10bit -> 8 bit", None))
        self.audioBox.setText(_translate("MainWindow", "Include separate audio", None))
        self.subBox.setText(_translate("MainWindow", "Include separate subtitles", None))
        self.label.setText(_translate("MainWindow", "Process with episodes from", None))
        self.label_2.setText(_translate("MainWindow", "to", None))
        self.menu.setTitle(_translate("MainWindow", "More", None))
        self.actionChoose.setText(_translate("MainWindow", "Choose Anime folder", None))
        self.actionCheck.setText(_translate("MainWindow", "Check tools", None))
        self.actionX264.setText(_translate("MainWindow", "Converter parameters", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))

    def open(self):
        folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", QtCore.QDir.currentPath())
        global anime
        anime = Anime(folder)
        #anime.bit()
        self.pathLabel.setText(folder)
        self.numLabel.setText(str(anime.n()))
        self.start.setMaximum(anime.n())
        self.end.setMaximum(anime.n())
        self.converter = Converter(self)
        self.convertBox.setChecked(False)
        self.audioBox.setChecked(False)
        self.subBox.setChecked(False)
        self.runButton.setDisabled(True)

    def set_convert(self, need):
        self.converter.need_convert = need
        self.runButton.setEnabled(need)

    def set_audio(self, need):
        if need:
            folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", anime.folder)
            if folder != '':
                self.converter.audio = [True, folder, '']
                print(self.converter.audio)
            else:
                print('No folder!')
                self.audioBox.setChecked(False)
        else:
            self.converter.audio = [False, '', '']
        self.runButton.setEnabled(need)

    def set_subs(self, need):
        if need:
            folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", anime.folder)
            if folder != '':
                self.converter.subs = [True, folder, '']
            else:
                print('No folder!')
                self.subBox.setChecked(False)
        else:
            self.converter.subs = [False, '', '']
        self.runButton.setEnabled(need)

    def bake(self):
        self.progressBar.setVisible(True)
        self.convertBox.setDisabled(True)
        self.audioBox.setDisabled(True)
        self.subBox.setDisabled(True)
        self.resetButton.setDisabled(True)
        self.runButton.setDisabled(True)
        self.start.setDisabled(True)
        self.end.setDisabled(True)
        self.converter.first = self.start.value()
        self.converter.last = self.end.value()
        self.converter.update.connect(self.progress, QtCore.Qt.QueuedConnection)
        self.converter.finished.connect(self.unlock, QtCore.Qt.QueuedConnection)
        self.converter.start()

    def progress(self):
        if self.progressBar.value() == -1:
            num = str(self.end.value() + 1 - self.start.value())
            self.progressBar.setFormat('%v/'+num)
            self.progressBar.setTextVisible(True)
            self.progressBar.setMaximum(self.end.value()-self.start.value()+1)
            print('Set bar length to:', self.end.value())
            self.progressBar.setValue(0)
        self.progressBar.setValue(self.progressBar.value()+1)
        print('Updated bar to:', self.progressBar.value())

    def unlock(self):
        self.convertBox.setDisabled(False)
        self.audioBox.setDisabled(False)
        self.subBox.setDisabled(False)
        self.resetButton.setDisabled(False)
        self.runButton.setDisabled(False)
        self.start.setDisabled(False)
        self.end.setDisabled(False)

    def abort(self):
        self.convertBox.setChecked(False)
        self.audioBox.setChecked(False)
        self.subBox.setChecked(False)

    def x264Dialog(self):
        Dialog = QtGui.QDialog()
        dui = x264_Dialog()
        dui.setupUi(Dialog, self.converter.params)
        if Dialog.exec_():
            self.converter.params = dui.getValues()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.open()
    MainWindow.show()
    sys.exit(app.exec_())
