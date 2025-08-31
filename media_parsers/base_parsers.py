from abc import ABC, abstractmethod

class BaseParser:
    def __init__(self, url: str):
        self.url = url


class SimpleDownloadParser(ABC, BaseParser):
    @abstractmethod
    def download_video(self) -> (dict, str):
        """
        Write here your code to download video and send its filename or a dictionary with necessary data, including filename
        :return: dictionary with video data or a string with video's filename
        """


class ResolutionDownloadParser(ABC, BaseParser):
    @abstractmethod
    def download_video_by_resolution(self, resolution) -> (dict, str):
        """
        Write here your code to download video with needed reslution and send its filename or a dictionary with necessary data, including filename
        :return: dictionary with video data or a string with video's filename
        """


class VideoInfoParser(ABC, BaseParser):
    @abstractmethod
    def get_video_info(self) -> dict:
        """
        Write here your code that parser should get video's info and send it

        :return: Return dictionary with necessary fields
        """