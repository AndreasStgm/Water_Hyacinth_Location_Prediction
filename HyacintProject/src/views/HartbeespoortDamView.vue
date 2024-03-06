<template>
  <div id="logo">
    <img src="../assets/logoCBC.jpg" height="300" alt="CBC logo"/>
  </div>
  <div id="right">
    <article id="buttonsTop">
      <button class="dayButtons">
        <RouterLink to="/hartbeespoortDam" class="routerLink">TODAY</RouterLink>
      </button>
      <button class="dayButtons">
        <RouterLink to="/hartbeespoortDam" class="routerLink">+ 1 DAY</RouterLink>
      </button>
      <button class="dayButtons">
        <RouterLink to="/hartbeespoortDam" class="routerLink">+2 DAYS</RouterLink>
      </button>
    </article>
    <article id="contentMap">
      <p id="date">03/03/2024</p>
      <img id="map" src="../assets/googleview.png" alt="GoogleMaps Map of Dam" width=100%/>
      <p id="accuracy">Accuracy: 83% </p>
      <button @click="$router.go(-1)" class="backButton">Back</button>
    </article>
  </div>
</template>

<script>

</script>

<style scoped>
body {
  position: relative;
}

#logo {
  float: left;
  width: 30%;
  text-align: center;
}

#logo img {
  margin-top: 50px;
}

#right {
  font-size: 30px;
  margin-top: 210px;
  padding-right: 2%;
  width: 70%;
  float: right;
}

#right p {
  text-align: right;
  padding: 10px 0;
}


.dayButtons {
  font-size: 30px;
  padding: 10px 30px;
  background-color: #707330;
  margin-left: 10px;
}

.routerLink {
  text-decoration: none;
  color: white;
}

.backButton {
  float: right;
  font-size: 30px;
  background-color: #707330;
  color: white;
  margin: 10px;
  padding: 10px 30px;
}


</style>