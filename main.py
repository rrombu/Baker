__author__ = "Roman Budnik"
__copyright__ = "Copyright 2014-2016"
__credits__ = ["Roman Budnik"]
__license__ = "LGPL"
__version__ = "0.9.7"
__maintainer__ = "Roman Budnik"
__status__ = "Development"

if __name__ == "__main__":
    import sys
    import json
    from gui import Ui_MainWindow
    from PyQt4 import QtGui
    from os import environ

    print("Baker started.")
    with open("config.json", "r") as f:
        settings = json.load(f)
        print("Settings loaded.")

    workdir = settings["tools_location"].replace("%appdata%", environ['APPDATA'])

    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.checksoft(workdir)
    ui.open()
    MainWindow.show()
    sys.exit(app.exec_())