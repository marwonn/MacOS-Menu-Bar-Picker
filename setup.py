#from os import times_result
from setuptools import setup

APP = ['statusbarApp.py']
DATA_FILES = ['logo.png', 'download.png', 'beer.png']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'logo.icns',
    'plist': {
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,
    },
    'packages': ['rumps','yt_dlp', 'clipboard', 'validators']
}

setup(
    app=APP,
    name='mtoolbox',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps','yt_dlp', 'clipboard', 'validators']
)
