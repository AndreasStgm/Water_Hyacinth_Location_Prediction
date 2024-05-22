<script setup lang="ts">
</script>

<template>
  <main>
    <h1>Water Hyacinth location BY Centre for Biological Control</h1>
    <img src="../../public/images/logoCBC.jpg" alt="CBC logo"/>
    <article id="buttons">
      <button>
        <RouterLink to="/hartbeespoortDam">Hartbeespoort Dam</RouterLink>
      </button>
      <button>
        <RouterLink to="/hartbeespoortDam">Other Dam</RouterLink>
      </button>
    </article>

  </main>
</template>

<style scoped>
h1 {
  text-align: center;
  margin: 50px auto 20px auto;
}

img {
  display: block;
  margin: 50px auto;
}

#buttons{
  text-align:center;
}

button {
  padding: 10px 30px;
  margin-left: 20px;
  background-color: #707330;
}

button > * {
  text-decoration: none;
  color: white;
}
</style>
