# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread
from subprocess import Popen, PIPE, call
import os
import probe

__author__ = "Roman Budnik"
__copyright__ = "Copyright 2014-2016"
__credits__ = ["Roman Budnik"]
__license__ = "LGPL"
__version__ = "0.9.7"
__maintainer__ = "Roman Budnik"
__status__ = "Development"


class Converter(QThread):
    if __name__ != "__main__":
        from PyQt4.QtCore import pyqtSignal
        update = pyqtSignal(list)
        finished = pyqtSignal()

    def __init__(self, anime, performance=""):
        import json
        import logging
        from collections import OrderedDict
        from os import environ, path, makedirs, chdir

        with open("config.json", "r") as f:
            global settings
            settings = json.load(f, object_pairs_hook=OrderedDict)
        logging.info("Settings loaded.")

        workdir = settings["tools_location"].replace("%appdata%", environ['APPDATA'])
        if not path.exists(workdir):
            makedirs(workdir)
        chdir(workdir)
        logging.debug("Working directory changed to {}".format(workdir))

        if __name__ != "__main__":
            super(Converter, self).__init__()
        self.need_convert = False
        self.audio = [False, 'path', 'items']
        self.subs = [False, 'path', 'items']
        self.first = 0
        self.last = 0
        self.params = ""
        if performance:
            self.params = "--preset {} ".format(performance)
        else:
            for flag in settings["x264"]:
                self.params += "--{} {} ".format(flag, settings["x264"][flag])
        self.verbose = False
        self.anime = anime
        logging.info("Converter initialized.")

    def setup(self, first, last, need_convert, audio=None, subs=None, verbose=False):
        if audio:
            self.audio = [True,
                          anime.audio[audio]["path"],
                          anime.audio[audio]["items"]]
        if subs:
            self.subs = [True,
                         anime.subtitles[subs]["path"],
                         anime.subtitles[subs]["items"]]
        self.first = first
        self.last = last
        self.need_convert = bool(need_convert)
        if verbose:
            self.verbose = True
        logging.info("Converter parameters set.")

    def x264(self, folder, file, extension):
        import atexit
        import logging

        logging.info("[x264] Converting:\n\t{} from {}".format(file, folder))
        preset = 'x264 --verbose {} -o "'.format(self.params)
        query = '{}{}.x264" "{}\\{}.{}"'.format(preset, file, folder, file, extension)
        frames_to_decode = probe.frames_total("{}\\{}.{}".format(folder, file, extension))
        completion = -1
        logging.info("[x264] Executing: {}".format(query))
        x = Popen(query, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)  # Pyinstaller needs everything piped
        atexit.register(x.kill)
        while x.returncode is None:
            x.poll()
            line = x.stderr.readline()
            logging.debug("[x264] {}".format(line))
            try:
                frame = line.decode().split('frame=')[-1].split()[0]
                frame = int(frame)
            except:
                continue
            progress = int(int(frame)/frames_to_decode*100)
            if progress != completion:
                try:
                    self.update.emit([None, progress])
                except RuntimeError:
                    print("{}%".format(progress))
                completion = progress
        if x.returncode != 0:
            logging.error("[x264][ERROR] x264 exited with code {}!".format(x.returncode))
            exit(1)
        else:
            logging.info("[x264] Conversion completed.")
        atexit.unregister(x.kill)

    def mkvmerge(self, folder, file, fonts):
        import logging

        logging.info("[mkvmerge] Merging:\n\t{} from {}".format(file, folder))
        if not os.path.exists(folder + '\\Baked'):
            os.makedirs(folder + '\\Baked')
        v = '"{}\\{}.mkv" '.format(folder, file)
        v8 = '"{}.x264" '.format(file)
        a = '--forced-track "0:yes" --default-track "0:yes" "{}\\{}.mka" '.format(self.audio[1], file)
        if os.path.exists('{}\\{}.ass'.format(self.subs[1], file)):
            s = '--forced-track "0:yes" --default-track "0:yes" "{}\\{}.ass" '.format(self.subs[1], file)
        elif os.path.exists('{}\\{}.надписи.ass'.format(self.subs[1], file)):
            s = '--forced-track "0:yes" --default-track "0:yes" "{}\\{}.надписи.ass" '.format(self.subs[1], file)
        else:
            logging.error('[mkvmerge] Sub file error!')
            s = ''
        query = 'mkvmerge -o "' + folder + '\\Baked\\' + file + '.mkv" '
        if self.need_convert:
            query += (v8 + '-D ')
        query += v
        if self.audio[0]:
            query += a
        if self.subs[0]:
            query += s
            if fonts:
                for folder in fonts:
                    for font in fonts[folder]:
                        query += '--attachment-mime-type application/octet-stream ' \
                                 '--attach-file "{}\{}" '.format(folder, font)
        logging.info("[mkvmerge] Executing: {}".format(query))
        if self.verbose:
            ret = call(query, shell=True, creationflags=0x08000000)
        else:
            ret = call(query, shell=True)
        if ret != 0:
            logging.error("[mkvmerge][ERROR] mkvmerge exited with code {}!".format(ret))
            exit(1)
        else:
            logging.info("[mkvmerge] Merging completed.")

    def run(self):
        import logging

        logging.info("Work started...")
        self.progress_counter = 0
        for i in range(self.first, self.last+1):
            if self.need_convert:
                self.x264(self.anime.folder, self.anime.episode(i-1), self.anime.v_ext)
            self.mkvmerge(self.anime.folder, self.anime.episode(i-1), self.anime.fonts)
            if self.need_convert:
                os.remove(self.anime.episode(i-1)+'.x264')
            self.progress_counter += 1
            try:
                self.update.emit([self.progress_counter, None])
            except RuntimeError:
                logging.info("Completed {} episode(s).".format(self.progress_counter))
        try:
            self.update.emit([None, 100])
            self.finished.emit()
        except RuntimeError:
            logging.info("Work finished.")

if __name__ == "__main__":
    import sys
    import json
    import logging
    from collections import OrderedDict
    from getopt import getopt
    from title import Anime
    from os import environ, path, makedirs, chdir

    fileLog = logging.FileHandler("Baker.log", 'w')
    fileLog.setLevel("WARNING")
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

    logging.info("Baker started.")
    convert = False
    verbose = False
    lightweight = False
    performance = False
    audio = False
    subtitles = False
    opts, args = getopt(sys.argv[1:], "p:a:s:f:t:P:cvd")
    '''
    p - Path to title folder
    a - name of the folder containing Audio
    s - name of the folder containing Subtitles
    f - From episode number
    t - To episode number
    P - performance mode (lightweight or ultrafast)
    c - file needs Conversion
    v - verbose output
    d - log level set to debug
    '''
    for opt, arg in opts:
        if opt == "-p":   workpath = arg
        elif opt == "-a": audio = arg
        elif opt == "-s": subtitles = arg
        elif opt == "-f": fromep = int(arg)
        elif opt == "-t": toep = int(arg)
        elif opt == "-c": convert = True
        elif opt == "-v": verbose = True
        elif opt == "-P": performance = arg
        elif opt == "-d":
            rootLogger.setLevel("DEBUG")
            fileLog.setLevel("DEBUG")

    with open("config.json", "r") as f:
        settings = json.load(f)
        logging.debug("Settings from configuration file loaded.")

    workdir = settings["tools_location"].replace("%appdata%", environ['APPDATA'])
    print(workdir)
    if not path.exists(workdir):
        makedirs(workdir)
        logging.debug("Working directory created at {}".format(workdir))

    if "workpath" not in locals():
        logging.error("Specify path with -p paramter!")
        input("Press ENTER to exit...")
        exit(1)
    if "fromep" not in locals():
        logging.error("Specify file number to start from with -f parameter!")
        exit(1)
    if "toep" not in locals():
        logging.error("Specify file number on which to end process with -f parameter!")
        exit(1)
    if not convert and not (audio or subtitles):
        logging.error("Nothing to pack and no conversion asked. Nothing to do here. Goodbye!")

    logging.info("Command line parameters read.")
    anime = Anime(workpath, workdir)
    converter = Converter(anime, performance=performance)
    converter.setup(fromep, toep, convert, audio, subtitles, verbose)
    converter.run()