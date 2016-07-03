class Anime():
    def __init__(self, path):
        from os import listdir, walk
        from probe import bit_depth

        self.folder = path
        self.episodes = []
        self.params = {'': False}
        self.audio = {}
        self.subtitles = {}
        self.fonts = {}

        tree = walk(path)
        for dir in tree:
            if (not dir[2] and dir[0] != path) or dir[0] == "{}\\Baked".format(path): # Only endpoint and root folder
                continue
            dir[2].sort()
            if any(entry for tag in ["mkv", "mp4", "m4v", "avi"] for entry in dir[2] if tag in entry):
                self.episodes = dir[2]
            if any(entry for tag in ["mka", "mp3", "aac", "flac"] for entry in dir[2] if tag in entry):
                title = dir[0][dir[0].rfind('\\')+1:]
                self.audio[title] = {"path":dir[0], "items":dir[2]}
            if any(entry for tag in ["ass", "srt"] for entry in dir[2] if tag in entry):
                title = dir[0][dir[0].rfind('\\')+1:]
                self.subtitles[title] = {"path":dir[0], "items":dir[2]}
            if any(entry for tag in ["ttf", "otf"] for entry in dir[2] if tag in entry):
                self.fonts[dir[0]] = dir[2]
        self.quantity = len(self.episodes)
        self.bit_depth = bit_depth('{}\\{}'.format(self.folder, self.episodes[0]))
        self.v_ext = self.episodes[0][-3:]

    def n(self):
        return self.quantity

    def list(self):
        return self.episodes

    def episode(self, n):
        print('episode :', self.episodes[n])
        return self.episodes[n][:-4]