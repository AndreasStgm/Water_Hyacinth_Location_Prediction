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

      google_height: 25.780000 - 25.720774,
      google_width: 27.907111 - 27.784343,
      picture_width: 1400,
      picture_height: 700,

      ellipseColors: ["#FF0000", "#00FF00", "#0000FF"],
      //needs to be a fetch/axios
      ellipses: [
        {
          "center_x": 757.4011593640796,
          "center_y": 275.9369515626647,
          "x_axis_length": 143.02009442334906,
          "y_axis_length": 309.5101140468501,
          "angle": 104.67786092704013
        },
        {
          "center_x": 767.8516224513011,
          "center_y": 368.0977904005568,
          "x_axis_length": 32.367357376641635,
          "y_axis_length": 63.5976247995742,
          "angle": 102.68584371568285
        },
        {
          "center_x": 784.3245172725781,
          "center_y": 381.2209580495952,
          "x_axis_length": 15.78464837881021,
          "y_axis_length": 40.12109110397098,
          "angle": 104.75481662216997
        }
      ]
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
        //coordinate bottom left corner training data : -25.780000, 27.784343
        //coordinate top right corner training data : -25.720778, 27.907111
        //coordinate bottom right corner training data : -25.780000, 27.907111

        this.ellipses.forEach((ellipse, index) => {
          const center = {lat: this.getX(ellipse.center_y), lng: this.getY(ellipse.center_x)};
          const semiMajorAxis = this.getEllipseWidth(ellipse.y_axis_length);
          const semiMinorAxis = this.getEllipseHeight(ellipse.x_axis_length);
          const angle = ellipse.angle;
          const points = this.generateEllipsePoints(center, semiMajorAxis, semiMinorAxis, 360, angle);

          const color = this.ellipseColors[index % this.ellipseColors.length]; // Get color based on index

          new google.maps.Polygon({
            paths: points,
            strokeColor: color,
            fillColor: color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            map: map
          });
        });
      };
    },
    generateEllipsePoints(center, semiMajorAxis, semiMinorAxis, numPoints, angle) {
      const points = [];
      const angleStep = (2 * Math.PI) / numPoints;
      const tiltAngle = angle * (Math.PI / 180);

      for (let i = 0; i < numPoints; i++) {
        const angle = i * angleStep;
        const x = semiMajorAxis * Math.cos(angle);
        const y = semiMinorAxis * Math.sin(angle);

        const rotatedX = x * Math.cos(tiltAngle) - y * Math.sin(tiltAngle);
        const rotatedY = x * Math.sin(tiltAngle) + y * Math.cos(tiltAngle);

        const lat = center.lat + rotatedX;
        const lng = center.lng + rotatedY;
        points.push({lat, lng});
      }
      return points;
    },
    getX(image_y) {
      const google_x = -25.720774;
      return google_x - image_y * this.getHeightStep();
    },
    getY(image_x) {
      const google_y = 27.784343;
      return google_y + image_x * this.getWidthStep();
    },
    getEllipseWidth(image_height) {
      return image_height * this.getHeightStep();
    },
    getEllipseHeight(image_width) {
      return image_width * this.getWidthStep();
    },
    getWidthStep() {
      return this.google_width / this.picture_width;  //0.00008769
    },
    getHeightStep() {
      return this.google_height / this.picture_height; //0.00008461
    }
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
