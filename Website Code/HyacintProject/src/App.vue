<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
*{
  box-sizing: border-box;
  font-family:Arial, Helvetica, sans-serif;
  text-shadow: -1px -1px 0 #979e4e, 1px -1px 0 #979e4e, -1px 1px 0 #979e4e, 1px 1px 0 #979e4e;
}

body{
  background-image: url("assets\hyacinth-background.jpg");
  color: white;
  font-size: 20px;
}

button {
  text-decoration: none;
  color: white;
}
</style>
