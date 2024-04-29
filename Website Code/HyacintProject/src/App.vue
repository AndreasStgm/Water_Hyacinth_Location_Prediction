<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
body{
  background-image: url("assets\hyacinth-background.jpg");
  color: white;
  font-size: 20px;
  font-family:Arial, Helvetica, sans-serif;
  text-shadow: -1px -1px 0 #707330, 1px -1px 0 #707330, -1px 1px 0 #707330, 1px 1px 0 #707330;
}

button {
  text-decoration: none;
  color: white;
  font-family:Arial, Helvetica, sans-serif;
  text-shadow: -1px -1px 0 #979e4e, 1px -1px 0 #979e4e, -1px 1px 0 #979e4e, 1px 1px 0 #979e4e;
}
</style>
