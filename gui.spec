# -*- mode: python -*-

block_cipher = None
single_file = True  # set before running pyinstaller


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Roman\\PycharmProjects\\Baker'],
             binaries=None,
             datas=[("config.json", "."),
                    ("README.md", "."),
                    ("resources\\splash", "resources"),
                    ("resources\\gui.ico", "resources")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
if single_file:
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name='Baker',
              debug=False,
              strip=False,
              upx=True,
              console=False , icon='resources\\gui.ico')
else:
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='Baker',
              debug=False,
              strip=False,
              upx=True,
              console=False , icon='resources\\gui.ico')
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='main')