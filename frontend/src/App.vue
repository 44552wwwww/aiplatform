<template>
  <div id="app">
    <AppHeader />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
</script>

<style scoped>
main {
  min-height: calc(100vh - 60px);
}
</style>
