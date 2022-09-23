# Anime Recommender System

## Intro

Anime Recommender System is for recommending animes to people. It uses Redis to store all the features and embeddings extracted by Spark MLlib. The backend is built with Flask. The model is trained by using TensorFlow. To make it more responsive, I also try to collect the users' behavior data and process it with Kafka and Flink, and then save it in the Redis.

## Tech Stack

- Flask
- Spark
- TensorFlow
- Kafka
- Redis
- Flink
- Faiss
