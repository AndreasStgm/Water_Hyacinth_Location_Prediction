import preprocessing_weather as preproc_wthr
import preprocessing_image as preproc_img


def main() -> None:
    preproc_wthr.drop_unneeded_columns()


if __name__ == "__main__":
    main()
