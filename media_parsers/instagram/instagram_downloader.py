import instaloader
from ..base_parser import BaseParser

class InstagramDownloader(BaseParser):
    def download_video(self):
        loader = instaloader.Instaloader(
            download_comments=False,
            download_pictures=False,
            download_geotags=False,
            download_video_thumbnails=False,
            save_metadata=False,
        )
        shortcode = self.url.split("/")[-2]

        try:
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            loader.download_post(post, target="vids")
            filename = f"{post.date.strftime('%Y-%m-%d')}_{post.date.strftime('%H-%M-%S')}_UTC.mp4"

            return {
                "title": filename,
                "caption": post.caption,
                "profile": post.profile,
            }

        except Exception as e:
            print(e)