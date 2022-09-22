<template>
  <div>
    <div v-if="!animePage" id="top">
      <h1>动漫推荐系统</h1>
      <h3>猜你喜欢:</h3>
      <button v-on:click="loadItems" type="button" class="btn btn-info">
        刷新
      </button>
    </div>

    <div v-else>
      <AnimeComp
        :id="currentAnime.anime_id"
        :japanese_title="currentAnime.japanese_title"
        :title="currentAnime.name"
        :img_url="currentAnime.image_url"
        :genres="currentAnime.genre"
        :aired="currentAnime.aired"
        :rating="currentAnime.rating"
        :members="currentAnime.members"
      >
      </AnimeComp>
      <br />
      <h3>相似推荐:</h3>
    </div>

    <div class="cell-grid">
      <div v-for="group in itemsGroup" :key="group" class="row">
        <div v-for="item in group" :key="item" class="col">
          <CellComp
            :id="item.anime_id"
            :japanese_title="item.japanese_title"
            :title="item.name"
            :img_url="item.image_url"
            :genres="item.genre"
          >
          </CellComp>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CellComp from './components/cell.vue'
import AnimeComp from './components/anime.vue'
import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'App',
  components: {
    CellComp,
    AnimeComp,
  },
  data() {
    return {
      items: [],
      currentAnime: {},
    }
  },
  computed: {
    itemsGroup() {
      console.log(_.chunk(this.items, 4))
      return _.chunk(this.items, 4)
    },
    animePage() {
      const path = window.location.pathname
      return path === '/anime'
    },
  },
  async created() {
    if (this.animePage) {
      await this.loadCurrentAnime()
    }
    await this.loadItems()
  },
  methods: {
    async loadItems() {
      const userId = this.getUserId()
      const animeId = this.getAnimeId()
      let url = 'http://localhost:5003/'
      if (!this.animePage) {
        url = `${url}recommends?user_id=${userId}`
      } else {
        url = `${url}sim?anime_id=${animeId}`
      }
      const res = await axios.get(url)
      this.items = res.data
    },
    async loadCurrentAnime() {
      const animeId = this.getAnimeId()
      const url = `http://localhost:5003/anime/${animeId}`
      const res = await axios.get(url)
      this.currentAnime = res.data
    },
    getUserId() {
      const params = new URLSearchParams(window.location.search)
      return params.get('user_id')
    },
    getAnimeId() {
      const params = new URLSearchParams(window.location.search)
      return params.get('anime_id')
    },
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.cell-grid {
  margin: 50px auto 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, 400px);
  grid-column-gap: 3em;
}
</style>
