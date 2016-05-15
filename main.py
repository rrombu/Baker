from os import environ, path, makedirs, chdir
appdata = '{}\\Baker'.format(environ['APPDATA'])
if not path.exists(appdata):
    makedirs(appdata)
chdir(appdata)

print('Main name: {}'.format(__name__))
if __name__ == "__main__":
    import sys
    from gui import Ui_MainWindow
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.checksoft(appdata)
    ui.open()
    MainWindow.show()
    sys.exit(app.exec_())