import rumps
import yt_dlp
import validators
import json
import os, subprocess, sys

# rumps.debug_mode(True)

APP_NAME = 'mtoolbox'
DOWNLOAD_PATH = os.path.join(os.path.expanduser('~') + '/Downloads/')

class StatusBarApp(rumps.App):
    def __init__(self):
        super(StatusBarApp, self).__init__(name=APP_NAME, icon='logo.png')
        self.menu = [rumps.MenuItem('Get Video!', icon='download.png', dimensions=(18, 18)), 
                     rumps.MenuItem('Brew Check!', icon='beer.png', dimensions=(18, 18)),
                     None]
        
    @rumps.clicked("Get Video!")
    def get_video(self, _):
        try:
            url = os.popen("""osascript -e 'tell app "safari" to get the url of the current tab of window 1'""").read()
            is_valid = validators.url(url)
            
            if is_valid:
                ydl_opts = {'outtmpl':f'{DOWNLOAD_PATH}%(title)s.%(ext)s',
                            'format': 'best',
                            'noplaylist': True,}

                metadaten = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)

                title = metadaten.get("title")
                extension = metadaten.get("ext")

                rumps.notification("Download of:", f"{title}.{extension}", "")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
                    ydl.download([url])

                # Open Finder after download has finished
                if os.path.exists(DOWNLOAD_PATH):
                    subprocess.call(["open", DOWNLOAD_PATH])
            else:
                rumps.notification("Invalid URL", "Check URL syntax.", "")
        except:
            rumps.notification("URL not supported!", "Check URL", "")
    
    @rumps.clicked("Brew Check!")
    def update_brew(self, _):
        os.popen('brew update')
        result = json.loads(os.popen('brew outdated --json').read())

        if len(result['formulae']) > 0 or len(result['casks']) > 0:
            no_of_updates = len(result['formulae']) + len(result['casks'])
            self.menu.add(f'Avaible updates: {no_of_updates}')

            for i in result['formulae']:
                self.menu.add(i['name'])
            
            for i in result['casks']:
                self.menu.add(i['name'])

            rumps.notification("Yes, updates available.", "", "")
        else:
            self.last_state = None
            rumps.notification("No updates available.", "", "")

    @rumps.clicked("refresh")
    def refresh_brew(self, _):
        os.execl(sys.executable, sys.executable, * sys.argv)

if __name__ == '__main__':
    StatusBarApp().run()
