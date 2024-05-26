from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pickle
from numpy import ndarray
from pandas import DataFrame
from sklearn.linear_model import LinearRegression


class Weather(BaseModel):  # Model for input data
    windspeed: float
    winddir: float


class Location(BaseModel):  # Model for output data
    center_x: float
    center_y: float
    x_axis_length: float
    y_axis_length: float
    angle: float


origins: list[str] = ["http://localhost:5173", "http://0.0.0.0:5173", "http://127.0.0.1:5173"]

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

# Loading in the model from the preprocessing
prediction_model: LinearRegression = pickle.load(open("model.pkl", "rb"))


@app.post("/predict", response_model=list[Location], status_code=status.HTTP_200_OK)
def get_prediction_from_model(input_weather: Weather) -> list[Location]:
    # Loading the input data into a dataframe with the correct labels for the columns
    input_df: DataFrame = DataFrame(columns=["windspeed", "winddir"])
    input_df.loc[len(input_df.index)] = [input_weather.windspeed, input_weather.winddir]

    # Calculating a prediction using the model
    prediction: ndarray = prediction_model.predict(input_df)

    # Converting the data into the response model
    result_locations: list[Location] = []
    new_location: Location
    for i in range(0, len(prediction[0]), 5):
        new_location = Location(center_x=prediction[0][i],
                                center_y=prediction[0][i+1],
                                x_axis_length=prediction[0][i+2],
                                y_axis_length=prediction[0][i+3],
                                angle=prediction[0][i+4])
        result_locations.append(new_location)

    return result_locations
