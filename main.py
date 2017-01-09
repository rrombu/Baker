__author__ = "Roman Budnik"
__copyright__ = "Copyright 2014-2016"
__credits__ = ["Roman Budnik"]
__license__ = "LGPL"
__version__ = "0.9.9"
__maintainer__ = "Roman Budnik"
__status__ = "Development"

if __name__ == "__main__":
    import sys
    import json
    import logging
    from gui import Ui_MainWindow
    from PyQt4 import QtGui
    from os import environ, path, makedirs

    fileLog = logging.FileHandler("Baker.log", 'w')
    fileLog.setLevel("INFO")
    consoleLog = logging.StreamHandler(stream=sys.stdout)
    consoleLog.setLevel("DEBUG")

    logFormatter = logging.Formatter("[{levelname:^7}] {message}", style='{')
    fileLog.setFormatter(logFormatter)
    consoleLog.setFormatter(logFormatter)

    rootLogger = logging.getLogger()
    rootLogger.setLevel("INFO")
    rootLogger.handlers = []
    rootLogger.addHandler(fileLog)
    rootLogger.addHandler(consoleLog)

    if "-d" in sys.argv:
        rootLogger.setLevel("DEBUG")
        fileLog.setLevel("DEBUG")

    with open("config.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
        logging.debug("Settings from configuration file loaded.")

    workdir = settings["tools_location"].replace("%appdata%", environ['APPDATA'])
    if not path.exists(workdir):
        makedirs(workdir)
        logging.debug("Working directory created at {}".format(workdir))

    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.checksoft(workdir)
    try:
        ui.open(workdir, collection=settings["open_path"])
    except KeyError:
        ui.open(workdir)
    MainWindow.show()
    sys.exit(app.exec_())