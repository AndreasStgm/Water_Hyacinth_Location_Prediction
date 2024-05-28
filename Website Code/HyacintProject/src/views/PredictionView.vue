<template>
  <section class="top">
    <article class="left">
      <img src="../../public/images/logoCBC.jpg" alt="CBC logo"/>
    </article>
    <article class="right">
      <section class="buttons-top">
        <button @click="drawGoogle(1)">TODAY</button>
        <button @click="drawGoogle(2)" class="day-buttons">+1 DAY</button>
        <button @click="drawGoogle(3)" class="day-buttons">+2 DAYS</button>
        <p class="date">{{ formatDate(myDate) }}</p>
      </section>
    </article>
  </section>

  <section class="under">
    <div id="map" class="map"></div>
    <button @click="$router.go(-1)">Back</button>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      myDate: new Date(),

      latitude: null,
      longitude: null,

      X: null,
      Y: null,
      X2: null,
      Y2: null,

      //Data from snapshot
      google_height: null,
      google_width: null,
      picture_width: 1400,
      picture_height: 700,

      googleMap: null,
      windspeed: null,
      winddir: null,

      ellipseColors: ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFA500", "#800080"],
      aiEllipses: [],
      drawnEllipses: []
    };
  },
  methods: {
    formatDate(date) {
      let day = date.getDate().toString().padStart(2, '0');
      let month = (date.getMonth() + 1).toString().padStart(2, '0');
      let year = date.getFullYear();
      return `${day}/${month}/${year}`;
    },
    getX(image_y) {
      return this.X - image_y * this.getHeightStep();
    },
    getY(image_x) {
      return this.Y + image_x * this.getWidthStep();
    },
    getEllipseWidth(image_height) {
      return image_height * this.getHeightStep();
    },
    getEllipseHeight(image_width) {
      return image_width * this.getWidthStep();
    },
    getWidthStep() {
      return this.google_width / this.picture_width;
    },
    getHeightStep() {
      return this.google_height / this.picture_height;
    },
    async initMap() {
      console.log('ini');
      //south east hemisphere
      this.google_height = this.X2 + this.X;
      this.google_width = this.Y2 - this.Y;

      const apiKey = 'AIzaSyAhgJ0hSYHjGBCwIm1B0G_zHW2vtAcQ6zo';
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=visualization&callback=initMapCallback`;
      script.async = true;

      if (this.googleMap == null) {
        // Define initMapCallback function
        window.initMapCallback = () => {
          this.googleMap = new google.maps.Map(document.getElementById('map'), {
            scrollwheel: true,
            mapTypeControl: false,
            center: {lat: this.latitude, lng: this.longitude},
            zoom: 14,
            streetViewControl: false,
            zoomControl: true,
          });
        };
        document.head.appendChild(script);
      }
    },
    async drawGoogle(day) {
      console.log('draw');

      try {
        await this.setWindspeedAndDirection(day);
        await this.getPrediction();
        this.removePreviousEllipse();
        this.drawEllipse();
        this.setDate(day);
      } catch (error) {
        console.error('Error with drawGoogle:', error);
      }
    },
    async setWindspeedAndDirection(day) {
      const weatherResponse = await axios.get(`https://api.open-meteo.com/v1/forecast?latitude=${this.latitude}&longitude=${this.longitude}&hourly=wind_speed_10m,wind_direction_10m&forecast_days=${day}`);
      this.windspeed = weatherResponse.data.hourly.wind_speed_10m[24 * (day - 1)];
      this.winddir = weatherResponse.data.hourly.wind_direction_10m[24 * (day - 1)];
    },
    async getPrediction() {
      const aiResponse = await axios.post(`http://localhost:8000/predict`, {
        windspeed: this.windspeed,
        winddir: this.winddir
      });
      this.aiEllipses = aiResponse.data;
    },
    removePreviousEllipse() {
      this.drawnEllipses.forEach(polygon => polygon.setMap(null));
      this.drawnEllipses = [];
    },
    drawEllipse() {
      this.aiEllipses.forEach((ellipse, index) => {
        const center = {lat: this.getX(ellipse.center_y), lng: this.getY(ellipse.center_x)};
        const semiMajorAxis = this.getEllipseWidth(ellipse.y_axis_length);
        const semiMinorAxis = this.getEllipseHeight(ellipse.x_axis_length);
        const angle = ellipse.angle;
        const points = this.generateEllipsePoints(center, semiMajorAxis, semiMinorAxis, 360, angle);

        const color = this.ellipseColors[index % this.ellipseColors.length]; // Get color based on index

        const polygon = new google.maps.Polygon({
          paths: points,
          strokeColor: color,
          fillColor: color,
          strokeOpacity: 0.8,
          strokeWeight: 2,
          map: this.googleMap
        });
        this.drawnEllipses.push(polygon);
      });
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
    setDate(day) {
      let dateToday = new Date();
      dateToday.setDate(dateToday.getDate() + (day - 1));
      this.myDate = new Date(dateToday);
    }
  },
  async mounted() {
    console.log('mount');
    console.log(this.googleMap);

    this.latitude = parseFloat(this.$route.query.latitude);
    this.longitude = parseFloat(this.$route.query.longitude);
    this.X = parseFloat(this.$route.query.X1);
    this.Y = parseFloat(this.$route.query.Y1);
    this.X2 = parseFloat(this.$route.query.X2);
    this.Y2 = parseFloat(this.$route.query.Y2);

    await this.initMap();
    await this.drawGoogle(1);
  },
}
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
