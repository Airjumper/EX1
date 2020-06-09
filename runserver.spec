# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['runserver.py'],
             pathex=['D:\\WSU\\Myaccessment\\accessment  semester 5\\PX\\codes\\EX1'],
             binaries=[],
             datas=[('EX1/templates', 'templates'), ('EX1/static', 'static'), ('EX1', 'EX1')],
             hiddenimports=[],
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
          name='runserver',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
