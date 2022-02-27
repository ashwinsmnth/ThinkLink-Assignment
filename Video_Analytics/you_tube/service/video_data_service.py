
from you_tube.service.db_connection import DBConnection


class VideoDataService(object):

    def __init__(self):
        self.db = DBConnection()

    def insert_video_analytics_into_db(self, video_id_to_details):
        """
        Inserts video analytics information into database
        :param video_id_to_details: Video ID to details
        :type video_id_to_details: dict
        :return:
        """
        data = []
        for video_id, details in video_id_to_details.items():
            data.append((video_id,
                         details["title"],
                         details["description"],
                         details["published_time"],
                         str(details["thumbnail_urls"])
                         ))

        self.db.insert_data(data)

    def get_last_published_video_recorded(self):
        """
        Gets last published video date recorded in database
        :return:
        """
        sql = """ SELECT MAX(published_time) FROM video_analytics; """
        response = self.db.execute_statement(sql, expecting_return=True)[0][0]
        return response if response else None

    def get_latest_you_tube_videos(self):
        """
        Gets latest YouTube videos stored in database
        :return:
        """
        result = []
        sql = """ SELECT * FROM video_analytics ORDER BY published_time DESC; """
        response = self.db.execute_statement(sql, expecting_return=True)
        for video_details in response:
            data = {
                "video_id": video_details[1],
                "title": video_details[2],
                "description": video_details[3],
                "published_time": video_details[4],
                "thumbnail_urls": video_details[5]
            }
            result.append(data)
        return result

    def search_videos_based_on_query(self, query=None):
        """
        Searches videos based on query param sent
        :return:
        """
        if not query:
            return self.get_latest_you_tube_videos()

        title_query, description_query = query.get("title"), query.get("description")
        if title_query and description_query:
            sql = """ SELECT * FROM video_analytics where title like '%{}%' and description like '%{}%' ORDER BY published_time DESC; """.format(title_query, description_query)
        elif title_query:
            sql = """ SELECT * FROM video_analytics where title like '%{}%' ORDER BY published_time DESC; """.format(title_query)
        elif description_query:
            sql = """ SELECT * FROM video_analytics where description like '%{}%' ORDER BY published_time DESC; """.format(description_query)
        else:
            sql = """ SELECT * FROM video_analytics ORDER BY published_time DESC; """

        result = []
        response = self.db.execute_statement(sql, expecting_return=True)
        for video_details in response:
            data = {
                "video_id": video_details[1],
                "title": video_details[2],
                "description": video_details[3],
                "published_time": video_details[4],
                "thumbnail_urls": video_details[5]
            }
            result.append(data)
        return result
