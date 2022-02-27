
import os

import googleapiclient.discovery
import googleapiclient.errors

from you_tube.util.constants import API_KEY

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class YouTubeDataRetrieverService(object):

    def __init__(self, video_data_service):
        self.video_data_service = video_data_service

    def process_latest_you_tube_videos(self):
        published_after = self.video_data_service.get_last_published_video_recorded()
        you_tube_data = YouTubeDataRetrieverService._retrieve_you_tube_video_information(published_after)
        self._insert_video_information_into_db(you_tube_data)

    @staticmethod
    def _retrieve_you_tube_video_information(published_after=None, max_results=50):
        """
        Retrieves latest videos sorted in reverse chronological order of their publishing date-time from YouTube
        :return: YouTube Data
        :rtype: dict
        """
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY)

        if published_after:
            request = youtube.search().list(
                part="snippet",
                maxResults=max_results,
                type="video",
                order="date",
                publishedAfter=published_after
            )
        else:
            request = youtube.search().list(
                part="snippet",
                maxResults=max_results,
                type="video",
                order="date"
            )

        return request.execute()

    def _insert_video_information_into_db(self, you_tube_data):
        """
        Inserts YouTube video information into database
        :param you_tube_data: YouTube Data
        :type you_tube_data: dict
        :return:
        """
        video_id_to_details = {}
        for video in you_tube_data["items"]:
            snippet_details = video["snippet"]
            thumbnail_urls = YouTubeDataRetrieverService._get_thumbnail_urls(snippet_details["thumbnails"])
            video_id_to_details[video["id"]["videoId"]] = {"title": snippet_details["title"],
                                                           "description": snippet_details["description"],
                                                           "published_time": snippet_details["publishedAt"],
                                                           "thumbnail_urls": thumbnail_urls}

        self.video_data_service.insert_video_analytics_into_db(video_id_to_details)

    @staticmethod
    def _get_thumbnail_urls(thumbnail_details):
        """
        Returns thumbnail urls from data.
        Input format:
            'thumbnails': {
                'default': {
                        'url': 'https://yt3.ggpht.com/ytc/AKedOLSsnWm_dQzIqM-qgW74yebXNX_b__k6WAeUBb6GeGQ=s88-c-k-c0x00ffffff-no-rj',
                        'width': 88, 'height': 88
                            },
                'medium': {
                            'url': 'https://yt3.ggpht.com/ytc/AKedOLSsnWm_dQzIqM-qgW74yebXNX_b__k6WAeUBb6GeGQ=s240-c-k-c0x00ffffff-no-rj',
                            'width': 240, 'height': 240
                        },
                'high': {'url': 'https://yt3.ggpht.com/ytc/AKedOLSsnWm_dQzIqM-qgW74yebXNX_b__k6WAeUBb6GeGQ=s800-c-k-c0x00ffffff-no-rj',
                        'width': 800, 'height': 800}
            }
        :param thumbnail_details:
        :return:
        """
        thumbnail_urls = []
        for _, value in thumbnail_details.items():
            thumbnail_urls.append(value["url"])
        return thumbnail_urls
