from recall.context import Context
from typing import List
from recall.model.LSH import get_item_lsh
from recall.dataset.embedding import get_one_item_embedding
import time
import recall.strategy as strategy
import concurrent.futures
from recall import util

strategies: List[strategy.RecallStrategy] = [
    strategy.MostRatedStrategy(),
    strategy.HighRatedStrategy(),
    strategy.UserEmbeddingStrategy(),
    strategy.RecentClickStrategy(),
]

# experiments:
# A - strategy[0 + 1]
# B - strategy[0 + 1 + 2]


def anime_recall(context: Context, n=20) -> List[int]:

    # experiment_strategies = strategies[:2]
    # bucket = util.bucketize(context.user_id, 2)
    # if bucket == 1:
    #     experiment_strategies = strategies

    with concurrent.futures.ThreadPoolExecutor() as executor:
        outputs = executor.map(lambda s: run_strategy(s, context, n), strategies)
        outputs = [a_id for lst in outputs for a_id in lst]
        outputs = list(dict.fromkeys(outputs))
        # return [{'anime_id': id, 'ab:recall': bucket} for id in outputs]
        return outputs


def similar_animes(context: Context, n=20) -> List[int]:
    lsh = get_item_lsh()
    target_item_emb = get_one_item_embedding(context.anime_id)
    if target_item_emb is None:
        return []
    outputs = lsh.search(target_item_emb, n=n)
    return outputs


def run_strategy(strategy: strategy.RecallStrategy, context: Context, n):
    start_time = time.time()
    res = strategy.recall(context, n)
    elapse_time = time.time() - start_time
    print('Strategy %s took %.2fms' % (strategy.name(), elapse_time * 1000))
    return res
