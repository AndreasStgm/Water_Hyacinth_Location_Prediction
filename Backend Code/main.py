import preprocessing_weather as preproc_wthr
import preprocessing_image as preproc_img

import pandas as pd

PATH_TO_IMAGES: str = "./training_data/Sentinel2"
PATH_TO_PROCESSED_DATA: str = "./training_data/processed_data"

PREPROCESS: bool = True


def gather_data_and_preprocess() -> tuple[pd.DataFrame, pd.DataFrame]:
    # First we drop all unneeded columns from the weather data
    weather_df: pd.DataFrame = preproc_wthr.drop_unneeded_columns()
    # Write it to a csv file for safekeeping and easy viewing
    weather_df.to_csv(f"{PATH_TO_PROCESSED_DATA}/preprocessed_weather_hartbeespoort.csv", index=False)

    # Get a list of all the images in the folder
    images: list[str] = preproc_img.get_all_images_in_folder(PATH_TO_IMAGES, True)

    # Create a new dataframe with the structure fo the first image
    images_df: pd.DataFrame = preproc_img.convert_image_to_dataframe_row(images[0])
    for i in range(1, len(images)):
        images_df = pd.concat([images_df, preproc_img.convert_image_to_dataframe_row(images[i])])
    # Write it to a csv file for safekeeping and easy viewing
    images_df.to_csv(f"{PATH_TO_PROCESSED_DATA}/preprocessed_image_test.csv", index=False)

    # Dropping rows in the weather data that are before the first and after the last image
    weather_df.drop(weather_df[weather_df["datetime"] < images_df["datetime"].min()].index, inplace=True)
    weather_df.drop(weather_df[weather_df["datetime"] > images_df["datetime"].max()].index, inplace=True)

    # Remove rows in the weather data where we have no image data for
    # Since according to the researchers the hyacinth moves across the lake in a couple of hours,
    # it doesn't really matter what happen in between the days of the images
    filtered_weather_df: pd.DataFrame = pd.DataFrame(columns=weather_df.columns)
    for item in weather_df.values:
        if item[0] in images_df["datetime"].values:
            filtered_weather_df.loc[len(filtered_weather_df.index)] = item

    filtered_weather_df.to_feather(f"{PATH_TO_PROCESSED_DATA}/preprocessed_weather_hartbeespoort.feather")
    images_df.to_feather(f"{PATH_TO_PROCESSED_DATA}/preprocessed_image_test.feather")

    return filtered_weather_df, images_df


def main() -> None:
    weather_df: pd.DataFrame
    images_df: pd.DataFrame

    if PREPROCESS:
        result_data: tuple[pd.DataFrame, pd.DataFrame] = gather_data_and_preprocess()
        weather_df = result_data[0]
        images_df = result_data[1]
    else:
        weather_df = pd.read_feather(f"{PATH_TO_PROCESSED_DATA}/preprocessed_weather_hartbeespoort.feather")
        images_df = pd.read_feather(f"{PATH_TO_PROCESSED_DATA}/preprocessed_image_test.feather")

    print(len(weather_df))
    print(len(images_df))


if __name__ == "__main__":
    main()
