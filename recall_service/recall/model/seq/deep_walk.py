from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, collect_list
from collections import defaultdict
from pyspark.sql.session import SparkSession
from recall.config import config
import numpy as np
import dill
import os

rng = np.random.default_rng()


def build_seq(rating_df: DataFrame, spark: SparkSession):
    entrance_items = None
    entrance_probs = None
    transfer_probs = None

    if os.path.isfile('output/entrance_items.dill'):
        with open('output/entrance_items.dill', 'rb') as f:
            entrance_items = dill.load(f)
        with open('output/entrance_probs.dill', 'rb') as f:
            entrance_probs = dill.load(f)
        with open('output/transfer_probs.dill', 'rb') as f:
            transfer_probs = dill.load(f)
        print('loaded model from file')
    else:
        os.mkdir('output')
        rating_df = rating_df.where('rating > 7')

        watch_seq_df = rating_df.groupBy('user_id').agg(
            collect_list(col('anime_id').cast('string')).alias('anime_ids')
        )

        watch_seq = watch_seq_df.collect()
        watch_seq = [s['anime_ids'] for s in watch_seq]
        matrix = defaultdict(lambda: defaultdict(int))

        for i in range(len(watch_seq)):
            seq = watch_seq[i]
            add_seq_to_matrix(seq, matrix)

        transfer_probs = {k: get_transfer_prob(v) for k, v in matrix.items()}

        counts = {k: sum(neighbors.values()) for k, neighbors in matrix.items()}
        entrance_items = list(transfer_probs.keys())
        total_count = sum(counts.values())
        entrance_probs = [counts[k] / total_count for k in entrance_items]

        with open('output/entrance_items.dill', 'wb') as f:
            dill.dump(entrance_items, f)
        with open('output/entrance_probs.dill', 'wb') as f:
            dill.dump(entrance_probs, f)
        with open('output/transfer_probs.dill', 'wb') as f:
            dill.dump(transfer_probs, f)
        print('save model to file')

    n = config['deepwalk']['sample_count']
    length = config['deepwalk']['sample_length']
    samples = []
    for i in range(n):
        s = one_random_walk(length, entrance_items, entrance_probs, transfer_probs)
        samples.append(s)

    return spark.createDataFrame([[row] for row in samples], ['anime_ids'])


def add_seq_to_matrix(seq, m):
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            a = seq[i]
            b = seq[j]
            if a == b:
                continue
            m[a][b] += 1
            m[b][a] += 1


def get_transfer_prob(vs):
    neighbors = vs.keys()
    total_weight = sum(vs.values())
    probs = [vs[k] / total_weight for k in neighbors]
    try:
        assert abs(1.0 - sum(probs)) < 0.000000001
    except:
        print(sum(probs))
        print(vs)

    return {'neighbors': list(neighbors), 'probs': probs}


def one_random_walk(length, entrance_items, entrance_probs, transfer_probs):
    start_vertex = rng.choice(entrance_items, 1, p=entrance_probs)[0]
    path = [str(start_vertex)]

    curr_vertex = start_vertex
    for _ in range(length):
        if curr_vertex not in transfer_probs:
            print(f'bad vertex {curr_vertex}')
            break

        neighbors = transfer_probs[curr_vertex]['neighbors']
        trans_prob = transfer_probs[curr_vertex]['probs']

        try:
            next_vertex = rng.choice(neighbors, 1, p=trans_prob)[0]
            path.append(str(next_vertex))
            curr_vertex = next_vertex
        except Exception as e:
            print(curr_vertex, e)
            break

    return path
