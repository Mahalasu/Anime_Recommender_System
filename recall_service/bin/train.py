from pyspark.sql import SparkSession
from recall.dataset.anime import spark_load_ratings
from recall.model import item2vec
from recall.dataset import embedding
from recall.model.seq import deep_walk

spark = SparkSession.builder.appName('recall').getOrCreate()

rating_df = spark_load_ratings(spark)
anime_seq = deep_walk.build_seq(rating_df, spark)
print('sample gen done')
(item_emb_df, user_emb_df) = item2vec.train_item2vec(anime_seq, rating_df)
print('embedding trained')

item_vec = item_emb_df.collect()
item_emb = {}
for row in item_vec:
    item_emb[row.word] = row.vector.toArray()

embedding.save_item_embedding(item_emb)

user_vec = user_emb_df.collect()
user_emb = {}
for row in user_vec:
    user_emb[row.user_id] = row.user_emb
embedding.save_user_embedding(user_emb)
print('item2vec embedding done')
