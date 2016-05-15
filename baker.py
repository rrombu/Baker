# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread
import os
import subprocess
import probe


class Converter(QThread):
    if __name__ != "__main__":
        from PyQt4.QtCore import pyqtSignal
        from PyQt4.QtCore import QThread
        update = pyqtSignal(list)
        finished = pyqtSignal()

    def __init__(self, anime):
        if __name__ != "__main__":
            super(Converter, self).__init__()
        self.need_convert = False
        self.audio = [False, 'path', 'params']
        self.subs = [False, 'path', 'params']
        self.first = 0
        self.last = 0
        self.params = '--preset slower --tune animation --profile high --level 4.2 --crf 17 --fps 23.976'
        self.params_easy = '--threads 1 --tune animation --profile high --level 4.2 --crf 17 --fps 23.976'
        self.verbose = False
        self.anime = anime

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
                self.x264(self.anime.folder, self.anime.episode(i-1), self.anime.v_ext)
            self.mkvmerge(self.anime.folder, self.anime.episode(i-1))
            if self.need_convert:
                os.remove(self.anime.episode(i-1)+'.x264')
            self.progress_counter += 1
            self.update.emit([self.progress_counter, None])
        self.update.emit([None, 100])
        self.finished.emit()

if __name__ == "__main__":
    from title import Anime
    path = ''
    anime = Anime(path)
    converter = Converter(None, anime)