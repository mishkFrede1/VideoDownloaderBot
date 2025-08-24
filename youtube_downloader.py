from yt_dlp import YoutubeDL

url = "https://www.youtube.com/watch?v=ZHfS8Q8-OtQ"
# url = "https://www.youtube.com/watch?v=R3GfuzLMPkA"


class YoutubeDownloader:
    def __init__(self, url: str):
        self.url = url

    def get_video_info(self):
        with YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False, process=False)
            title = info.get("title")
            thumbnail = info.get("thumbnail")
            uploader = info.get("uploader")
            duration = info.get("duration")
            formats = []
            for format in info.get("formats", []):
                formats.append(format.get('height'))

            return {
                "title": title,
                "thumbnail": thumbnail,
                "uploader": uploader,
                "duration": duration,
                "formats": formats
            }

    def download_video_by_resolution(self, resolution):
        ydl_opts = {
            'format': f'bv*[height<={resolution}]+ba/best',
            'outtmpl': '%(title)s.%(ext)s',
            'ffmpeg_location': r"H:\ffmpeg",
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
            info = ydl.extract_info(self.url, download=False, process=False)
            title = info.get("title")
            duration = info.get("duration")
            return {
                "title": title,
                "ext": "mp4",
                "duration": duration,
            }