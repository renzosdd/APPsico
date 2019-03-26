# -*- mode: python -*-

block_cipher = None


a = Analysis(['APPsico.py'],
             pathex=['C:\\Users\\renzo\\Documents\\GitHub\\APPSICO'],
             binaries=[],
             datas=[],
             hiddenimports=['sys', 'smtplib', 'datetime', 'email.message', 're', 'tkcalendar', 'tkinter', 'babel.numbers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='APPsico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='APPsico.ico')
