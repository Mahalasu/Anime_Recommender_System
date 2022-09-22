from recall.strategy import RecallStrategy
import recall.dataset.anime as dataset
from random import sample


class MostRatedStrategy(RecallStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.build_pool()

    def name(self):
        return 'Most Rated'

    def build_pool(self):
        (anime_df, _) = dataset.load_dataset()
        sorted_df = anime_df.sort_values(by=['members'], ascending=False)
        self.pool = sorted_df.iloc[:1000].index.to_list()
        print(f'{self.name()} pool loaded.')

    def recall(self, context, n=20):
        return sample(self.pool, n)
