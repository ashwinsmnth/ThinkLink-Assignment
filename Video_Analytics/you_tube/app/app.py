
from uwsgidecorators import cron, mulemsg, postfork, timer

from you_tube.api.api import VideoAnalyticsInfoApi, VideoAnalyticsSearchApi
from you_tube.api.cherrypy_utils import RootApi, start
from you_tube.service.video_data_service import VideoDataService
from you_tube.service.you_tube_data_retriever_service import YouTubeDataRetrieverService

YT_DATA_RETRIEVER_MULE_ID = 1
YT_DATA_RETRIEVER_MULE = "mule{}".format(YT_DATA_RETRIEVER_MULE_ID)


def init():
    video_data_service = VideoDataService()
    you_tube_data_retriever_svc = YouTubeDataRetrieverService(video_data_service)

    @timer(10, target=YT_DATA_RETRIEVER_MULE)
    def run_update(num):
        """
        Cron job to retrieve latest you tube data for every 10 seconds
        """
        print("Triggered scheduled update of recent you tube videos")
        you_tube_data_retriever_svc.process_latest_you_tube_videos()
        print("Completed scheduled update of recent you tube videos")

    video_analytics_root_api = RootApi()
    video_analytics_root_api.info = VideoAnalyticsInfoApi(video_data_service)
    video_analytics_root_api.search = VideoAnalyticsSearchApi(video_data_service)

    return start(video_analytics_root_api)


# uwsgi looks for a variable called "application" when it runs this file
application: init()
