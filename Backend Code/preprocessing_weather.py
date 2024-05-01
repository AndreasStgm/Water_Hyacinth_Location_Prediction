import pandas as pd


weather_raw: pd.DataFrame = pd.read_csv("./training_data/weather_hartbeespoort_raw.csv")

# Dropping unneeded columns
weather_raw = weather_raw.drop(["name", "tempmax", "tempmin", "temp", "feelslikemax", "feelslikemin", "feelslike", "dew", "humidity", "precip",
                                "precipprob", "precipcover", "preciptype", "snow", "snowdepth", "windgust", "sealevelpressure", "cloudcover",
                                "visibility", "solarradiation", "solarenergy", "uvindex", "severerisk", "sunrise", "sunset", "moonphase",
                                "conditions", "description", "icon", "stations"], axis=1)

weather_raw.to_csv("./training_data/processed_data/preprocessed_weather_hartbeespoort.csv")
