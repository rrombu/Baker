class Anime():
    def __init__(self, path):
        from os import listdir
        from probe import bit_depth
        self.episodes = []
        self.params = {'': False}
        self.folder = path
        content = listdir(self.folder)
        for item in content:
            if '.mkv' in item:
                self.episodes.append(item)
                self.v_ext = 'mkv'
            elif '.mp4' in item:
                self.episodes.append(item)
                self.v_ext = 'mp4'
        self.episodes.sort()
        self.quantity = len(self.episodes)
        self.bit_depth = bit_depth('"{}\\{}.{}"'.format(self.folder, self.episode(0), self.v_ext))

    def n(self):
        return self.quantity

    def list(self):
        return self.episodes

    def episode(self, n):
        print('episode :', self.episodes[n])
        return self.episodes[n][:-4]