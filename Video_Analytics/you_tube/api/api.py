import cherrypy


class VideoAnalyticsInfoApi(object):
    exposed: bool = True

    def __init__(self, video_data_service):
        self.video_data_service = video_data_service

    def GET(self):
        return self.video_data_service.get_latest_you_tube_videos()


class VideoAnalyticsSearchApi(object):

    def __init__(self, video_data_service):
        self.video_data_service = video_data_service

    def POST(self, request_data):
        # request_data = get_json_content()
        query_data = request_data.get("query")

        if request_data and "query" not in request_data:
            raise cherrypy.HTTPError(message="POST body is not in proper format.")
        if query_data and ("title" not in query_data and "description" not in query_data):
            raise cherrypy.HTTPError(message="POST body is not in proper format. "
                                             "Ony title and/or description is accepted as search parameter.")

        return self.video_data_service.search_videos_based_on_query(query_data)
