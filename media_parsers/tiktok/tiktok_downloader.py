import pyktok
import shutil
from ..base_parser import BaseParser

class TiktokDownloader(BaseParser):
    def download_video(self):
        pyktok.specify_browser('firefox')
        pyktok.save_tiktok(self.url, True)
        splt_url = self.url.split('/')
        filename = f"{splt_url[3]}_{splt_url[4]}_{splt_url[5].split('?')[0]}.mp4"
        shutil.move(filename, f"vids/{filename}")
        return filename
