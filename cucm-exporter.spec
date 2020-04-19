# -*- mode: python ; coding: utf-8 -*-
import ciscoaxl
from pathlib import Path
import os
import gooey
# gooey_root = os.path.dirname(gooey.__file__)
# gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix = 'gooey/languages')
# gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix = 'gooey/images')

block_cipher = None

a = Analysis(['cucm-exporter.py'],
             pathex=[Path.cwd()],
             binaries=[],
             datas=[('img', 'img'), ('TEMPLATE', 'TEMPLATE'),('img','gooey/images'),
                (f'{ciscoaxl.__path__[0]}/schema/8.5/*', 'ciscoaxl/schema/8.5.'),
                (f'{ciscoaxl.__path__[0]}/schema/10.0/*', 'ciscoaxl/schema/10.0.'),
                (f'{ciscoaxl.__path__[0]}/schema/10.5/*', 'ciscoaxl/schema/10.5.'),
                (f'{ciscoaxl.__path__[0]}/schema/11.0/*', 'ciscoaxl/schema/11.0.'),
                (f'{ciscoaxl.__path__[0]}/schema/11.5/*', 'ciscoaxl/schema/11.5.'),
                (f'{ciscoaxl.__path__[0]}/schema/12.0/*', 'ciscoaxl/schema/12.0.'),
                (f'{ciscoaxl.__path__[0]}/schema/12.5/*', 'ciscoaxl/schema/12.5.'),
                (f'{ciscoaxl.__path__[0]}/schema/current/*', 'ciscoaxl/schema/current/.')
                ],
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
         #  gooey_languages, # Add them in to collected files
         #  gooey_images, # Same here.
          name='cucm-exporter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
         icon="img/program_icon.ico" )
