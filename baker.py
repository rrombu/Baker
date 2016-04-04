# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import os
import subprocess
import probe

dir_path = '{}\\Baker'.format(os.environ['APPDATA'])
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
os.chdir(dir_path)

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
                self.v_ext = 'mkv'
            elif '.mp4' in item:
                self.episodes.append(item)
                self.v_ext = 'mp4'
        self.episodes.sort()
        self.quantity = len(self.episodes)
        startupinfo = subprocess.STARTUPINFO()  # Hide separate window
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.bit_depth = probe.bit_depth('"{}\\{}.{}"'.format(self.folder, self.episode(0), self.v_ext))

    def n(self):
        return self.quantity

    def list(self):
        return self.episodes

    def episode(self, n):
        print('episode :', self.episodes[n])
        return self.episodes[n][:-4]


class Converter(QtCore.QThread):
    update = QtCore.pyqtSignal(list)
    finished = QtCore.pyqtSignal()

    def __init__(self, mw):
        super(Converter, self).__init__()
        self.need_convert = False
        self.audio = [False, 'path', 'params']
        self.subs = [False, 'path', 'params']
        self.first = 0
        self.last = 0
        self.params = '--tune animation --profile high --level 4.2 --crf 17 --fps 23.976 --preset fast'
        self.verbose = False

    def x264(self, folder, file, extension):
        preset = 'x264 --verbose {} -o "'.format(self.params)
        query = '{}{}.x264" "{}\\{}.{}"'.format(preset, file, folder, file, extension)
        print(query)
        frames_to_decode = probe.frames_total("{}\\{}.{}".format(folder, file, extension))
        print('Total frames to decode: {}'.format(frames_to_decode))
        x = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while x.poll() is None:
            line = x.stderr.readline()
            try:
                frame = line.decode().split('frame=')[-1].split()[0]
                frame = int(frame)
            except:
                continue
            progress = int(int(frame)/frames_to_decode*100)
            self.update.emit([None, progress])

    def mkvmerge(self, folder, file):
        if not os.path.exists(folder + '\\Baked'):
            os.makedirs(folder + '\\Baked')
        v = '"' + folder + '\\' + file + '.mkv" '
        v8 = '"' + file + '.x264" '
        a = '--forced-track "0:yes" --default-track "0:yes" "' + self.audio[1] + '\\' + file + '.mka" '
        if os.path.exists('{}\\{}.ass'.format(self.subs[1], file)):
            s = '--forced-track "0:yes" --default-track "0:yes" "' + self.subs[1] + '\\' + file + '.ass" '
        elif os.path.exists('{}\\{}.надписи.ass'.format(self.subs[1], file)):
            s = '--forced-track "0:yes" --default-track "0:yes" "' + self.subs[1] + '\\' + file + '.надписи.ass" '
        else:
            print('Sub file error!')
            s = ''
        query = 'mkvmerge -o "' + folder + '\\Baked\\' + file + '.mkv" '
        if self.need_convert:
            query += (v8 + '-D ')
        query += v
        if self.audio[0]:
            query += a
        if self.subs[0]:
            query += s
        if self.verbose:
            subprocess.call(query, shell=True, creationflags=0x08000000)
        else:
            subprocess.call(query, shell=True)

    def run(self):
        self.progress_counter = 0
        for i in range(self.first, self.last+1):
            if self.need_convert:
                self.x264(anime.folder, anime.episode(i-1), anime.v_ext)
            self.mkvmerge(anime.folder, anime.episode(i-1))
            if self.need_convert:
                os.remove(anime.episode(i-1)+'.x264')
            self.progress_counter += 1
            self.update.emit([self.progress_counter, None])
        self.update.emit([None, 100])
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
        MainWindow.resize(300, 320)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.titleInfoBox = QtGui.QGroupBox(self.centralwidget)
        self.titleInfoBox.setObjectName(_fromUtf8("titleInfoBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.titleInfoBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.tPathLabel = QtGui.QLabel(self.titleInfoBox)
        self.tPathLabel.setObjectName(_fromUtf8("tPathLabel"))
        self.horizontalLayout_6.addWidget(self.tPathLabel)
        self.vPathLabel = QtGui.QLabel(self.titleInfoBox)
        self.vPathLabel.setObjectName(_fromUtf8("vPathLabel"))
        self.horizontalLayout_6.addWidget(self.vPathLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.tTitleLabel = QtGui.QLabel(self.titleInfoBox)
        self.tTitleLabel.setObjectName(_fromUtf8("tTitleLabel"))
        self.horizontalLayout_5.addWidget(self.tTitleLabel)
        self.vTitleLabel = QtGui.QLabel(self.titleInfoBox)
        self.vTitleLabel.setObjectName(_fromUtf8("vTitleLabel"))
        self.horizontalLayout_5.addWidget(self.vTitleLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.tNumLabel = QtGui.QLabel(self.titleInfoBox)
        self.tNumLabel.setObjectName(_fromUtf8("tNumLabel"))
        self.horizontalLayout_4.addWidget(self.tNumLabel)
        self.vNumLabel = QtGui.QLabel(self.titleInfoBox)
        self.vNumLabel.setObjectName(_fromUtf8("vNumLabel"))
        self.horizontalLayout_4.addWidget(self.vNumLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tBitLabel = QtGui.QLabel(self.titleInfoBox)
        self.tBitLabel.setObjectName(_fromUtf8("tBitLabel"))
        self.horizontalLayout_3.addWidget(self.tBitLabel)
        self.vBitLabel = QtGui.QLabel(self.titleInfoBox)
        self.vBitLabel.setObjectName(_fromUtf8("vBitLabel"))
        self.horizontalLayout_3.addWidget(self.vBitLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tAudioLabel = QtGui.QLabel(self.titleInfoBox)
        self.tAudioLabel.setObjectName(_fromUtf8("tAudioLabel"))
        self.horizontalLayout_2.addWidget(self.tAudioLabel)
        self.vAudioLabel = QtGui.QLabel(self.titleInfoBox)
        self.vAudioLabel.setObjectName(_fromUtf8("vAudioLabel"))
        self.horizontalLayout_2.addWidget(self.vAudioLabel)
        self.tSubLabel = QtGui.QLabel(self.titleInfoBox)
        self.tSubLabel.setObjectName(_fromUtf8("tSubLabel"))
        self.horizontalLayout_2.addWidget(self.tSubLabel)
        self.vSubLabel = QtGui.QLabel(self.titleInfoBox)
        self.vSubLabel.setObjectName(_fromUtf8("vSubLabel"))
        self.horizontalLayout_2.addWidget(self.vSubLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.titleInfoBox)
        self.settingsTabs = QtGui.QTabWidget(self.centralwidget)
        self.settingsTabs.setObjectName(_fromUtf8("settingsTabs"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.videoLayout = QtGui.QHBoxLayout()
        self.videoLayout.setObjectName(_fromUtf8("videoLayout"))
        self.convertVideoCheck = QtGui.QCheckBox(self.tab)
        self.convertVideoCheck.setObjectName(_fromUtf8("convertVideoCheck"))
        self.videoLayout.addWidget(self.convertVideoCheck)
        self.eightBitButton = QtGui.QRadioButton(self.tab)
        self.eightBitButton.setObjectName(_fromUtf8("eightBitButton"))
        self.videoLayout.addWidget(self.eightBitButton)
        self.tenBitButton = QtGui.QRadioButton(self.tab)
        self.tenBitButton.setObjectName(_fromUtf8("tenBitButton"))
        self.videoLayout.addWidget(self.tenBitButton)
        self.verticalLayout_3.addLayout(self.videoLayout)
        self.audioLayout = QtGui.QHBoxLayout()
        self.audioLayout.setObjectName(_fromUtf8("audioLayout"))
        self.audioCheck = QtGui.QCheckBox(self.tab)
        self.audioCheck.setObjectName(_fromUtf8("audioCheck"))
        self.audioLayout.addWidget(self.audioCheck)
        self.audioBox = QtGui.QComboBox(self.tab)
        self.audioBox.setObjectName(_fromUtf8("audioBox"))
        self.audioLayout.addWidget(self.audioBox)
        self.audioPreviewButton = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.audioPreviewButton.sizePolicy().hasHeightForWidth())
        self.audioPreviewButton.setSizePolicy(sizePolicy)
        self.audioPreviewButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.audioPreviewButton.setObjectName(_fromUtf8("audioPreviewButton"))
        self.audioLayout.addWidget(self.audioPreviewButton)
        self.verticalLayout_3.addLayout(self.audioLayout)
        self.subtitlesLayout = QtGui.QHBoxLayout()
        self.subtitlesLayout.setObjectName(_fromUtf8("subtitlesLayout"))
        self.subCheck = QtGui.QCheckBox(self.tab)
        self.subCheck.setObjectName(_fromUtf8("subCheck"))
        self.subtitlesLayout.addWidget(self.subCheck)
        self.subBox = QtGui.QComboBox(self.tab)
        self.subBox.setObjectName(_fromUtf8("subBox"))
        self.subtitlesLayout.addWidget(self.subBox)
        self.verticalLayout_3.addLayout(self.subtitlesLayout)
        self.line = QtGui.QFrame(self.tab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.rangeFromLabel = QtGui.QLabel(self.tab)
        self.rangeFromLabel.setObjectName(_fromUtf8("rangeFromLabel"))
        self.horizontalLayout_7.addWidget(self.rangeFromLabel)
        self.startBox = QtGui.QSpinBox(self.tab)
        self.startBox.setMinimum(1)
        self.startBox.setObjectName(_fromUtf8("startBox"))
        self.horizontalLayout_7.addWidget(self.startBox)
        self.rangeToLabel = QtGui.QLabel(self.tab)
        self.rangeToLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rangeToLabel.setObjectName(_fromUtf8("rangeToLabel"))
        self.horizontalLayout_7.addWidget(self.rangeToLabel)
        self.endBox = QtGui.QSpinBox(self.tab)
        self.endBox.setMinimum(1)
        self.endBox.setObjectName(_fromUtf8("endBox"))
        self.horizontalLayout_7.addWidget(self.endBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.settingsTabs.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        #self.settingsTabs.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        #self.settingsTabs.addTab(self.tab_3, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.settingsTabs)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.bakeButton = QtGui.QPushButton(self.centralwidget)
        self.bakeButton.setObjectName(_fromUtf8("bakeButton"))
        self.horizontalLayout.addWidget(self.bakeButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.progressLabel = QtGui.QLabel(self.centralwidget)
        self.progressLabel.setObjectName(_fromUtf8("progressLabel"))
        self.horizontalLayout.addWidget(self.progressLabel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.folderButton = QtGui.QPushButton(self.centralwidget)
        self.folderButton.setObjectName(_fromUtf8("folderButton"))
        self.horizontalLayout.addWidget(self.folderButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.totalProgressBar = QtGui.QProgressBar(self.centralwidget)
        self.totalProgressBar.setProperty("value", 24)
        self.totalProgressBar.setTextVisible(False)
        self.totalProgressBar.setObjectName(_fromUtf8("totalProgressBar"))
        self.verticalLayout_2.addWidget(self.totalProgressBar)
        self.episodeProgressBar = QtGui.QProgressBar(self.centralwidget)
        self.episodeProgressBar.setMaximumSize(QtCore.QSize(16777215, 15))
        self.episodeProgressBar.setValue(0)
        self.episodeProgressBar.setTextVisible(False)
        self.episodeProgressBar.setMaximum(100)
        self.episodeProgressBar.setObjectName(_fromUtf8("episodeProgressBar"))
        self.verticalLayout_2.addWidget(self.episodeProgressBar)
        MainWindow.setCentralWidget(self.centralwidget)
        #self.menubar = QtGui.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 428, 18))
        #self.menubar.setObjectName(_fromUtf8("menubar"))
        #self.menuMore = QtGui.QMenu(self.menubar)
        #self.menuMore.setObjectName(_fromUtf8("menuMore"))
        #MainWindow.setMenuBar(self.menubar)
        #self.statusbar = QtGui.QStatusBar(MainWindow)
        #self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #MainWindow.setStatusBar(self.statusbar)
        #self.actionAbout = QtGui.QAction(MainWindow)
        #self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        #self.menuMore.addAction(self.actionAbout)
        #self.menubar.addAction(self.menuMore.menuAction())

        self.retranslateUi(MainWindow)
        self.settingsTabs.setCurrentIndex(0)
        self.convertVideoCheck.toggled.connect(lambda l: self.set_convert(l))
        self.audioCheck.toggled.connect(lambda l: self.set_audio(l))
        self.subCheck.toggled.connect(lambda l: self.set_subs(l))
        self.bakeButton.clicked.connect(self.bake)
        self.startBox.valueChanged.connect(lambda l: self.endBox.setMinimum(l))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.tTitleLabel.hide()
        self.vTitleLabel.hide()
        self.tAudioLabel.hide()
        self.vAudioLabel.hide()
        self.tSubLabel.hide()
        self.vSubLabel.hide()
        self.eightBitButton.hide()
        self.tenBitButton.hide()
        self.audioBox.hide()
        self.audioPreviewButton.hide()
        self.subBox.hide()
        self.tab_2.hide()
        self.tab_3.hide()
        self.totalProgressBar.hide()
        self.episodeProgressBar.hide()
        self.progressLabel.hide()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Baker", None))
        self.titleInfoBox.setTitle(_translate("MainWindow", "Title info", None))
        self.tPathLabel.setText(_translate("MainWindow", "Path:", None))
        self.vPathLabel.setText(_translate("MainWindow", "?", None))
        self.tTitleLabel.setText(_translate("MainWindow", "Title:", None))
        self.vTitleLabel.setText(_translate("MainWindow", "?", None))
        self.tNumLabel.setText(_translate("MainWindow", "Number of episodes:", None))
        self.vNumLabel.setText(_translate("MainWindow", "?", None))
        self.tBitLabel.setText(_translate("MainWindow", "Pixel color depth:", None))
        self.vBitLabel.setText(_translate("MainWindow", "?", None))
        self.tAudioLabel.setText(_translate("MainWindow", "Audio tracks availiable:", None))
        self.vAudioLabel.setText(_translate("MainWindow", "?", None))
        self.tSubLabel.setText(_translate("MainWindow", "Subtitles availiable:", None))
        self.vSubLabel.setText(_translate("MainWindow", "?", None))
        self.convertVideoCheck.setText(_translate("MainWindow", "Convert video", None))
        self.eightBitButton.setText(_translate("MainWindow", "to 8-bit", None))
        self.tenBitButton.setText(_translate("MainWindow", "to10-bit", None))
        self.audioCheck.setText(_translate("MainWindow", "Add audio track", None))
        self.audioPreviewButton.setText(_translate("MainWindow", "Preview", None))
        self.subCheck.setText(_translate("MainWindow", "Add subtitles", None))
        self.rangeFromLabel.setText(_translate("MainWindow", "Process episodes from", None))
        self.rangeToLabel.setText(_translate("MainWindow", "to", None))
        self.settingsTabs.setTabText(self.settingsTabs.indexOf(self.tab), _translate("MainWindow", "General", None))
        self.settingsTabs.setTabText(self.settingsTabs.indexOf(self.tab_2), _translate("MainWindow", "Video", None))
        self.settingsTabs.setTabText(self.settingsTabs.indexOf(self.tab_3), _translate("MainWindow", "Other", None))
        self.bakeButton.setText(_translate("MainWindow", "Bake!", None))
        self.progressLabel.setText(_translate("MainWindow", "TextLabel", None))
        self.folderButton.setText(_translate("MainWindow", "Choose folder", None))
        #self.menuMore.setTitle(_translate("MainWindow", "More", None))
        #self.actionAbout.setText(_translate("MainWindow", "About", None))

    def open(self):
        folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", QtCore.QDir.currentPath())
        global anime
        anime = Anime(folder)
        self.vPathLabel.setText(folder)
        self.vNumLabel.setText(str(anime.n()))
        self.vBitLabel.setText("{}bit".format(anime.bit_depth))
        self.startBox.setMaximum(anime.n())
        self.startBox.setValue(1)
        self.endBox.setMaximum(anime.n())
        self.endBox.setValue(anime.n())
        self.converter = Converter(self)
        self.converter.update.connect(self.progress, QtCore.Qt.QueuedConnection)
        self.convertVideoCheck.setChecked(False)
        self.audioCheck.setChecked(False)
        self.subCheck.setChecked(False)
        self.bakeButton.setDisabled(True)

    def checksoft(self):
        import urllib.request

        if not os.path.exists('splash'):
            urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=0BzO4LREgLV3SaVNiYlhseFlLM1k",
                                       "splash")
        splash_pix = QtGui.QPixmap("{}\\splash".format(dir_path))
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setBold(True)
        font.setPointSize(10)
        splash.setFont(font)
        splash.showMessage("{}Starting...".format('\n'*11),
                           QtCore.Qt.AlignAbsolute, QtCore.Qt.white)
        splash.show()
        if not (os.path.exists('ffprobe.exe') or os.path.exists('mkvmerge.exe') or os.path.exists('x264.exe')):
            splash.showMessage("{}Downloading necessary tools...".format('\n'*11),
                               QtCore.Qt.AlignAbsolute, QtCore.Qt.white)
            splash.show()
            urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=0BzO4LREgLV3SUW5NbkNYYUIzb2M",
                                       "baker_tools.zip")
            from zipfile import ZipFile
            with ZipFile('baker_tools.zip', "r") as z:
                z.extractall()
            os.remove("baker_tools.zip")
        else:
            splash.showMessage("{}Welcome to bakery!".format('\n'*11),
                               QtCore.Qt.AlignAbsolute, QtCore.Qt.white)
            import time
            time.sleep(1)
        splash.finish(None)

    def set_convert(self, need):
        self.converter.need_convert = need
        self.bakeButton.setEnabled(need)

    def set_audio(self, need):
        if need:
            folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", anime.folder)
            if folder != '':
                self.converter.audio = [True, folder, '']
                l = 0
                for name in os.listdir(folder):
                    if os.path.isfile(os.path.join(folder, name)):
                        l += 1
                if l != anime.n():
                    QtGui.QMessageBox.warning(MainWindow, 'Warning', 'Number of audio-tracks is not equal to number of '
                                                                     'episodes! Some results may become missing.',
                                              QtGui.QMessageBox.Ok)
            else:
                print('No folder!')
                self.audioCheck.setChecked(False)
        else:
            self.converter.audio = [False, '', '']
        self.bakeButton.setEnabled(need)

    def set_subs(self, need):
        if need:
            folder = QtGui.QFileDialog.getExistingDirectory(MainWindow, "Choose folder", anime.folder)
            if folder != '':
                self.converter.subs = [True, folder, '']
                l = 0
                for name in os.listdir(folder):
                    if os.path.isfile(os.path.join(folder, name)):
                        l += 1
                if l != anime.n():
                    QtGui.QMessageBox.warning(MainWindow, 'Warning', 'Number of subtitles is not equal to number of '
                                                                     'episodes! Some results may become missing.',
                                              QtGui.QMessageBox.Ok)
            else:
                print('No folder!')
                self.subCheck.setChecked(False)
        else:
            self.converter.subs = [False, '', '']
        self.bakeButton.setEnabled(need)

    def bake(self):
        self.totalProgressBar.setMaximum(0)
        self.totalProgressBar.setValue(-1)
        self.totalProgressBar.setTextVisible(False)
        self.totalProgressBar.setVisible(True)
        self.convertVideoCheck.setDisabled(True)
        self.audioCheck.setDisabled(True)
        self.subCheck.setDisabled(True)
        self.bakeButton.setDisabled(True)
        self.startBox.setDisabled(True)
        self.endBox.setDisabled(True)
        self.episodeProgressBar.setValue(0)
        self.episodeProgressBar.show()
        self.converter.first = self.startBox.value()
        self.converter.last = self.endBox.value()
        self.converter.finished.connect(self.unlock, QtCore.Qt.QueuedConnection)
        self.converter.start()

    def progress(self, counters):
        if counters[0] is not None:
            if self.totalProgressBar.value() == -1:
                self.totalProgressBar.setFormat('%v/{}'.format(self.endBox.value() + 1 - self.startBox.value()))
                self.totalProgressBar.setTextVisible(True)
                self.totalProgressBar.setMaximum(self.endBox.value() - self.startBox.value() + 1)
                print('Set bar length to:', self.endBox.value())
                self.totalProgressBar.setValue(0)
            self.totalProgressBar.setValue(counters[0])
            print('Updated bar to:', self.totalProgressBar.value())
        if counters[1] is not None:
            self.episodeProgressBar.setValue(counters[1])

    def unlock(self):
        self.convertVideoCheck.setDisabled(False)
        self.audioCheck.setDisabled(False)
        self.subCheck.setDisabled(False)
        self.bakeButton.setDisabled(False)
        self.startBox.setValue(self.endBox.value())
        self.startBox.setDisabled(False)
        self.endBox.setValue(anime.n())
        self.endBox.setDisabled(False)

    def abort(self):
        self.convertVideoCheck.setChecked(False)
        self.audioCheck.setChecked(False)
        self.subCheck.setChecked(False)

    def x264Dialog(self):
        Dialog = QtGui.QDialog()
        dui = x264_Dialog()
        dui.setupUi(Dialog, self.converter.params)
        if Dialog.exec_():
            self.converter.params = dui.getValues()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.checksoft()
    ui.open()
    MainWindow.show()
    sys.exit(app.exec_())