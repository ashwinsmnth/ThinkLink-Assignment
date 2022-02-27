# ThinkLink-Assignment
Repository holding source code for ThinkLink Assignment

# Pre-requisite
-> docker and docker-compose it installed

# Instructions to run the server
-> git clone https://github.com/ashwinsmnth/ThinkLink-Assignment.git
-> cd ThinkLink-Assignment/Video_Analytics
-> Create api_keys.env file with content in key value format and multiple api keys can be provided with comma separated
   ex: API_KEYS="KEY1,KEY2,..."
-> docker-compose build
-> docker-compose up

# Note: https://www.docker.com/play-with-docker can be used to execute above procedure online if local setup is not available

# Instructions to test the API
-> Endpoint 1: /video-analytics/info
   -> GET call

-> Endpoint 2: /video-analytics/search
   -> POST call
   -> Sample Body:
      -> ex1: No body -> Should return all stored video information like /info method
      -> ex2: {"query": {"title": "Russia"}} -> Should return only those videos whose title has Russia in it
      -> ex3: {"query": {"description": "GMM25"}} -> Should return only those videos whose description has GMM25 in it
      -> ex4: {"query": {"title": "Russia", "description": "GMM25"}} -> Should return only those videos whose title has Russia and description has GMM25 in it
