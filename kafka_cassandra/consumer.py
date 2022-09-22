from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv
import json
import os
import datetime

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

load_dotenv('.env')

cloud_config = {'secure_connect_bundle': './secure-connect-anime-recommend-system.zip'}
auth_provider = PlainTextAuthProvider(
    os.environ.get('ASTRA_ID'), os.environ.get('ASTRA_KEY')
)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
print('Cassandra connected')


def cosume_kafka():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group-0',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    )

    return consumer


for item in cosume_kafka():
    event = item.value
    print(event)

    session.execute(
        f'''
        INSERT INTO user_behaviors.{KAFKA_TOPIC} (user_id, anime_id, happened_at)
        VALUES (%s, %s, %s)
        ''',
        (
            int(event['user_id']),
            int(event['anime_id']),
            datetime.datetime.fromtimestamp(event['happened_at']),
        ),
    )
