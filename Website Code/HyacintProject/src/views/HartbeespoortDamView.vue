<template>
  <section class="top">
    <article class="left">
      <img src="../../public/images/logoCBC.jpg" alt="CBC logo"/>
    </article>
    <article class="right">
      <section class="buttons-top">
        <button>
          <router-link to="/hartbeespoortDam" class="router-link">TODAY</router-link>
        </button>
        <button class="day-buttons">
          <router-link to="/hartbeespoortDam" class="router-link">+1 DAY</router-link>
        </button>
        <button class="day-buttons">
          <router-link to="/hartbeespoortDam" class="router-link">+2 DAYS</router-link>
        </button>
        <p class="date">{{ formatDate(myDate) }}</p>
      </section>
    </article>
  </section>

  <section class="under">
    <div id="map" class="map"></div>
    <p id="accuracy">Accuracy: {{ accuracy }}% </p>
    <button @click="$router.go(-1)">Back</button>
  </section>
</template>

<script>
export default {
  data() {
    return {
      myDate: new Date(),
      accuracy: 88,
    };
  },
  methods: {
    formatDate(date) {
      let day = date.getDate().toString().padStart(2, '0');
      let month = (date.getMonth() + 1).toString().padStart(2, '0');
      let year = date.getFullYear();
      return `${day}/${month}/${year}`;
    },
    initMap() {
      const apiKey = 'AIzaSyAhgJ0hSYHjGBCwIm1B0G_zHW2vtAcQ6zo';
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=visualization&callback=initMapCallback`;
      script.async = true;
      document.head.appendChild(script);

      window.initMapCallback = () => {
        const map = new google.maps.Map(document.getElementById('map'), {
          scrollwheel: true,
          mapTypeControl: false,
          center: {lat: -25.7500, lng: 27.8533},
          zoom: 14,
          streetViewControl: false,
          zoomControl: true,
        });
        //coordinate top left corner training data : -25.720774, 27.784343

        const center = {lat: -25.7500, lng: 27.8533}; // lat = up/down and lng = left/right
        const semiMajorAxis = 0.003; // Adjust for desired width of the ellipse
        const semiMinorAxis = 0.006; // Adjust for desired height of the ellipse
        const points = this.generateEllipsePoints(center, semiMajorAxis, semiMinorAxis, 360);

        new google.maps.Polygon({
          paths: points,
          strokeColor: "#FF0000",
          strokeOpacity: 0.8,
          strokeWeight: 2,
          map: map
        });
      };
    },
    generateEllipsePoints(center, semiMajorAxis, semiMinorAxis, numPoints) {
      const points = [];
      const angleStep = (2 * Math.PI) / numPoints;

      for (let i = 0; i < numPoints; i++) {
        const angle = i * angleStep;
        const lat = center.lat + (semiMajorAxis * Math.cos(angle));
        const lng = center.lng + (semiMinorAxis * Math.sin(angle));
        points.push({lat, lng});
      }
      return points;

    },
  },
  mounted() {
    this.initMap();
  },
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
}

.buttons-top button {
  padding: 10px 20px;
  margin: 3px 5px;
  width: 100px;
  background-color: #707330;
}

.under {
  width: 80%;
  margin: 10px auto;
}

.map {
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

.map {
  outline-style: solid;
}

@media (max-width: 845px) {
  .right {
    justify-content: flex-start;
  }

  .buttons-top {
    flex: 0;
  }

  .date {
    align-self: end;
    margin-left: 0;
  }
}
</style>
