# International Research Project - Water Hyacinth Location Prediction

This project is divided into two folders, backend and frontend. The frontend is a Vue.js application which calls the backend application for a new prediction based on windspeed and direction. These values are gathered from the [open-meteo API](https://github.com/open-meteo/open-meteo) and are passed to the prediction backend. This then returns a value of an ellipse that approximates the predicted location of the mat on the lake.

## Deployment

Have Docker installed, then run the following command:

```bash
docker compose up
```

The frontend application is hosted on `localhost:5173` and the backend documentation of the API can be found at `localhost:8000/docs`.
