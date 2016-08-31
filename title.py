__author__ = "Roman Budnik"
__copyright__ = "Copyright 2014-2016"
__credits__ = ["Roman Budnik"]
__license__ = "LGPL"
__version__ = "0.9.9"
__maintainer__ = "Roman Budnik"
__status__ = "Development"

class Anime():
    def __init__(self, path, tooldir):
        import logging
        from os import walk
        from probe import bit_depth

        logging.debug("> title.Anime.__init__ : {}".format(path))
        self.folder = path
        self.episodes = []
        self.params = {'': False}
        self.audio = {}
        self.subtitles = {}
        self.fonts = {}

        tree = walk(path)
        for dir in tree:
            logging.debug("\tAnalyzing {}".format(dir[0]))
            if (not dir[2] and dir[0] != path) or dir[0] == "{}\\Baked".format(path):  # Only endpoint and root folder
                logging.debug("\t\tskipped")
                continue
            dir[2].sort()
            if any(entry for tag in [".mkv", ".mp4", ".m4v", ".avi"] for entry in dir[2] if tag in entry):
                logging.debug("\t\tvideo")
                if self.episodes:  # dirty trick for skipping subfolders with videos
                    logging.debug("\t\t\talready filled - skipping")
                else:
                    self.episodes = dir[2]
            elif any(entry for tag in [".mka", ".mp3", ".aac", ".flac"] for entry in dir[2] if tag in entry):
                logging.debug("\t\taudio")
                title = dir[0][dir[0].rfind('\\')+1:]
                self.audio[title] = {"path":dir[0], "items": dir[2]}
            elif any(entry for tag in ["ass", "srt"] for entry in dir[2] if tag in entry):
                logging.debug("\t\tsubtitles")
                title = dir[0][dir[0].rfind('\\')+1:]
                self.subtitles[title] = {"path":dir[0], "items":dir[2]}
            elif any(entry for tag in [".ttf", ".otf"] for entry in dir[2] if tag in entry):
                logging.debug("\t\tfonts")
                self.fonts[dir[0]] = dir[2]
            else:
                logging.debug("\t\tnone")
        self.quantity = len(self.episodes)
        logging.info("Found {} episodes".format(self.quantity))
        self.bit_depth = bit_depth('{}\\{}'.format(self.folder, self.episodes[0]), tooldir)
        self.v_ext = self.episodes[0][-3:]
        logging.debug("\tVideo format is {}".format(self.v_ext))
        logging.debug("< title.Anime.__init__")

    def n(self):
        return self.quantity

    def list(self):
        return self.episodes

    def episode(self, n):
        return self.episodes[n][:-4]