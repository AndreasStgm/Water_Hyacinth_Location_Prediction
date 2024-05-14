import preprocessing_weather as preproc_wthr
import preprocessing_image as preproc_img

import pandas as pd

PATH_TO_IMAGES: str = "./training_data/Sentinel2"
PATH_TO_PROCESSED_DATA: str = "./training_data/processed_data"
TEST_IMAGE: str = "./training_data/Sentinel2/20230116_Sentinel2_Hartbeespoort.png"


def main() -> None:
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

    weather_df.to_feather(f"{PATH_TO_PROCESSED_DATA}/preprocessed_weather_hartbeespoort.feather")
    images_df.to_feather(f"{PATH_TO_PROCESSED_DATA}/preprocessed_image_test.feather")


if __name__ == "__main__":
    main()
