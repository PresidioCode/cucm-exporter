# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['cucm-exporter.py'],
             pathex=['C:\\Users\\bradh\\OneDrive - Presidio Networked Solutions, Inc\\code\\cucm-axl-examples'],
             binaries=[],
             datas=[('TEMPLATE/email-template.html', 'TEMPLATE/.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/8.5/*', 'ciscoaxl/schema/8.5.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/10.0/*', 'ciscoaxl/schema/10.0.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/10.5/*', 'ciscoaxl/schema/10.5.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/11.0/*', 'ciscoaxl/schema/11.0.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/11.5/*', 'ciscoaxl/schema/11.5.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/12.0/*', 'ciscoaxl/schema/12.0.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/12.5/*', 'ciscoaxl/schema/12.5.'),
                ('.venv/Lib/site-packages/ciscoaxl/schema/current/*', 'ciscoaxl/schema/current/.')
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
          name='cucm-exporter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
