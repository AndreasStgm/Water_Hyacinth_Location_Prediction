<template>
  <section class="top">
    <article class="left">
      <img src="../assets/logoCBC.jpg" alt="CBC logo"/>
    </article>
    <article class="right">
      <section class="buttonsTop">
        <button>
          <RouterLink to="/hartbeespoortDam" class="routerLink">TODAY</RouterLink>
        </button>
        <button class="dayButtons">
          <RouterLink to="/hartbeespoortDam" class="routerLink">+1 DAY</RouterLink>
        </button>
        <button class="dayButtons">
          <RouterLink to="/hartbeespoortDam" class="routerLink">+2 DAYS</RouterLink>
        </button>
        <p class="date">{{ formatDate(myDate) }}</p>
      </section>
    </article>
  </section>

  <section class="under">
    <iframe class="map-iframe" style="border:0" loading="lazy" allowfullscreen
            src="https://www.google.com/maps/embed/v1/view?zoom=14&center=-25.7500,27.8533&key=AIzaSyAhgJ0hSYHjGBCwIm1B0G_zHW2vtAcQ6zo"></iframe>
    <p id="accuracy">Accuracy: {{ getAccuracy() }}% </p>
    <button @click="$router.go(-1)">Back</button>
  </section>
</template>

<script>
export default {
  data() {
    return {
      myDate: new Date(),
      accuracy: null,
    };
  },
  methods: {
    formatDate(date) {
      let day = date.getDate().toString().padStart(2, '0');
      let month = (date.getMonth() + 1).toString().padStart(2, '0');
      let year = date.getFullYear();
      return `${day}/${month}/${year}`;
    },
    getAccuracy() {
      this.accuracy = 88;
      return this.accuracy;
    }
  }
};

</script>

<style scoped>
.top {
  margin: 10px auto;
  width: 80%;
  height: 190px;
  overflow: hidden;
  display: flex;
}

.left {
  text-align: left;
}

.left img {
  max-width: 100%;
  max-height: 100%;
}

.right {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  flex: 1;
  margin-left: 15px;
}

.date {
  float: right;
  margin-left: 10px;
  padding: 10px 0;
}


.buttonsTop button {
  padding: 10px 20px;
  margin: 3px 5px;
  width: 100px;
  background-color: #707330;
}

.under {
  width: 80%;
  margin: 10px auto;
}

.map-iframe {
  display: block;
  width: 100%;
  height: 70vh;
}

.under p {
  display: block;
  margin-top: 10px;
  float: right;
}

.under button {
  clear: right;
  float: right;
  background-color: #707330;
  margin: 10px;
  padding: 10px 20px;
}

a {
  text-decoration: none;
  color: white;
}

.map-iframe {
  outline-style: solid;
}

@media (max-width: 830px) {
  .right{
    justify-content: flex-start;
  }
  .buttonsTop {
    flex: 0;
  }

  .date {
    align-self: end;
    margin-left: 0;
  }
}


</style>