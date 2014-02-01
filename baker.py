import os

workdir = 'driveletter:\\folder\\anime\\'

class Scaner:
    episodes = []
    folders = []    
    def __init__(self,path):
        content = os.listdir(path)
        for item in content:
            p = workdir+item
            if os.path.isdir(p):
                self.folders.append(item)
                check = os.listdir(p)
                for o in check:
                    if os.path.isdir(p+'\\'+o):
                        self.folders.append(item+'\\'+o)
            else: self.episodes.append(item)
        self.episodes.sort()
        self.quantity = len(self.episodes)

    def list_folders(self):
        n = 1
        print('\nFolders included:')
        for folder in self.folders:
            print('   ',n,':',folder)
            n += 1

    def getfolder(self,n):
        return self.folders[n-1]

    def gettypes(self,folder1,folder2):
        a_type = ''
        s_type = ''
        if folder1 != folder2:
            a_type = os.listdir(folder1)[0].split(sep='.')[1]
            s_type = os.listdir(folder2)[0].split(sep='.')[1]
        else:
            a_types = ['mka','acc','ac3','flac']
            s_types = ['srt','ass']
            for file in os.listdir(folder1):
                extension = file.split(sep='.')[1]
                if extension in a_types: a_type = extension
                elif extension in s_types: s_type = extension
                if a_type != '' and s_type != '': break
        return(a_type,s_type)

    def howmany(self):
        return self.quantity

class Episode:
    def __init__(self,name,a_folder,s_folder,a_type,s_type):
        self.name = name[:-4]
        self.video = workdir + name[:-4] + '.mkv'
        self.audio = a_folder + '\\' + name[:-4] + '.' + a_type
        self.subs = s_folder + '\\' + name[:-4] + '.' + s_type

    def check(self):
        print('\nEpisode:',self.name,'\nA:',self.audio,'\nS:',self.subs)

    def ten2eight(self):
        preset = 'x264 --quiet --tune animation --profile high --level 4.2 --crf 20 --fps 23.976 --preset slower -o "'
        query = preset + self.name + '.x264" "' + self.video + '"'
        os.system(query)

    def repack(self):
        query = 'mkvmerge -o "' + workdir + '8bit\\' + self.name + '.mkv" -A "' + self.name + '.x264" --forced-track "0:yes" --default-track "0:yes" "' + self.audio + '" --forced-track "0:yes" --default-track "0:yes" "' + self.subs + '"'
        os.system(query)

    def letsgo(self):
        print('\n   Baking video from', self.name)
        self.ten2eight()
        print('\n   Converted! Packing sound and subtitles...\n')
        self.repack()
        self.name = self.name + '.x264'
        os.remove(self.name)
        print('\n   Episode', self.name, 'baked! Enjoy your meal! :3\n')
    
class Series:

    def __init__(self, workdir):
        self.folder = workdir
        print('\nWORKING WITH:',self.folder)
        content = Scaner(self.folder)
        self.quantity = content.howmany()
        print('\n# of episodes:',self.quantity)
        content.list_folders()
        self.audio_folder = workdir + content.getfolder(int(input('\nChoose AUDIO folder: ')))
        self.subtitles_folder = workdir + content.getfolder(int(input('Choose SUBTITLES folder: ')))
        self.types = content.gettypes(self.audio_folder, self.subtitles_folder)
        self.episodes = []
        for s in content.episodes:
            self.episodes.append(Episode(s,self.audio_folder,self.subtitles_folder,self.types[0],self.types[1]))

    def bake(self):
        i = 1
        start = int(input('Work with episodes starting with: '))
        n = int(input('And how many episodes are you up to? '))
        while i<self.quantity:
            if i>=start:
                self.episodes[i-1].letsgo()
                n -= 1
            i += 1
            if n == 0: break
        print("Enough cooking. That's all.")
            
print("\nLet's bake some 8bit single-file anime episodes!")
s = Series(workdir)
s.bake()
    
