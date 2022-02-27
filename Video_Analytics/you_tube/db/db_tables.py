

SQL_CREATE_VIDEO_ANALYTICS_TABLE = """ CREATE TABLE IF NOT EXISTS video_analytics (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        video_id varchar(75) NOT NULL,
                                        title varchar(255) NOT NULL,
                                        description varchar(512) NOT NULL,
                                        published_time datetime NOT NULL,
                                        thumbnail_urls varchar(1024) NOT NULL
                                    ); """


SQL_INDEX_CREATION = """ CREATE INDEX IF NOT EXISTS index_published_time ON video_analytics(published_time); """

VIDEO_ANALYTICS_DATABASE_TABLE = "video_analytics"

VIDEO_ANALYTICS_DB_COLUMNS = "video_id, title, description, published_time, thumbnail_urls"
