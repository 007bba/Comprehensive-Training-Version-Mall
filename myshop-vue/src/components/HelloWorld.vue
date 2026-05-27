<template>
  <div class="hello">
    <h1>{{ $store.state.count }}</h1>
    <button @click="addclick(1)">+</button>
    <button @click="reduceclick(1)">-</button>

      <div>异步操作</div>
    <div>
      <button @click="async_add(5)">异步增加</button>
      <button @click="async_reduce(5)">异步减少</button>
    </div>
    <h1>我是getters{{ count }}</h1>
  </div>
</template>

<script>
import {mapMutations,mapActions,mapGetters} from 'vuex'
export default {
  name: 'HelloWorld',
  methods: {
    ...mapMutations({
        addclick:'mutationAdd'
    }),



    //addclick(n){
    //  this.$store.commit('mutationAdd',n);
    //},



    ...mapMutations({
        reduceclick:'mutationReduce'
    }),



    //reduceclick(n){
      //this.$store.commit('mutationReduce',n);
    //},


    ...mapActions({
        async_add:'actionsAdd'
    }),



    //async_add(n){
    //  this.$store.dispatch('actionsAdd',n)
    //},



    ...mapActions({
      async_reduce:'actionsReduce'
    }),


    //async_reduce(n){
    //  this.$store.dispatch('actionsReduce',n)
    //}


  },
  computed:{
    ...mapGetters({
        count:'getCount'
    }),
    //count(){
    //  return this.$store.getters.getCount
    //}
  }
}
</script>