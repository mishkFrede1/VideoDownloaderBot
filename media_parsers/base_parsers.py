from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, url: str, has_video_info: bool):
        self.url = url
        self.has_video_info = has_video_info

    def get_video_info(self):
        if not self.has_video_info:
            return None

        return self._extract_video_info()

    @abstractmethod
    def _extract_video_info(self) -> dict:
        """
        Write here your code that parser should get video's info and send it

        :return: Return dictionary with necessary fields
        """

    @abstractmethod
    def download_video(self) -> (dict, str):
        """
        Write here your code to download video and send it's filename or a dictionary with necessary data, including filname
        :return: dictionary with video data or a string with video's filename
        """