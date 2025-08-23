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
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
            info = ydl.extract_info(self.url, download=False, process=False)
            title = info.get("title")
            ext = info.get("ext")
            return {
                "title": title,
                "ext": ext,
            }

# print(YoutubeDownloader(url).get_video_info())

# ydl_opts = {
#     'format': 'bv*[height<=720]+ba/best',
#     'outtmpl': '%(title)s.%(ext)s',
#     'ffmpeg_location': r"H:\ffmpeg",
# }
# with YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(url, download=False)
#     print("Title:", info.get("title"))
#     print("Thumbnail:", info.get("thumbnail"))
#     print("Uploader:", info.get("uploader"))
#     print("Duration:", info.get("duration"))
#     print("\nAvailable formats:")
#     for f in info.get("formats", []):
#         print(f"{f['format_id']} - {f.get('ext')} - {f.get('height')}p - {f.get('filesize', 'unknown')} bytes")
#
#     ydl.download([url])
