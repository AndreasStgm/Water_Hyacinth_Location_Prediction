import cv2
import numpy as np
import pandas as pd

from cv2.typing import MatLike
from typing import Sequence


DEBUG: bool = True
TEST_IMAGE: str = "training_data/Sentinel2/20230104_Sentinel2_Hartbeespoort.png"
KERNEL_SIZE: int = 3
EROSION_DILATION_ITR: int = 1


def main() -> None:
    # Read the image from the file
    image: MatLike = cv2.imread(TEST_IMAGE)

    if DEBUG:  # Display the image
        cv2.imshow(f"{TEST_IMAGE} - Full Res", image)
        cv2.waitKey(0)

    # Blurring the image to try reduce noise
    smoothed_image: MatLike = cv2.GaussianBlur(image, (KERNEL_SIZE, KERNEL_SIZE), 0)

    if DEBUG:
        cv2.imshow(f"{TEST_IMAGE} - Smoothed", smoothed_image)
        cv2.waitKey(0)

    # Detecting and green of the lake
    # Perfect green and blue have a hue of 120 and 240 respectively
    # OpenCV HSV maximum hue value is 360/2, so perfects are 60 and 120 respectively
    # https://docs.opencv.org/4.x/da/d97/tutorial_threshold_inRange.html
    hsv_image: MatLike = cv2.cvtColor(smoothed_image, cv2.COLOR_BGR2HSV)

    # Threshold values were obtained emperically
    # These thresholds are ideal for the Sentinel2 optical image
    lower_green: np.ndarray = np.array([55, 50, 112])  # Value is set to around 50%, because the BGR value of the green surface is 0, 128, 0
    upper_green: np.ndarray = np.array([65, 255, 144])  # With a max value of 256, 128 is exactly this 50%

    # These thresholds are ideal for the Sentinel1 radar image
    # lower_green: np.ndarray = np.array([55, 50, 50])  # Value is set to be within 20% and 100%
    # upper_green: np.ndarray = np.array([65, 255, 255])

    # These thresholds are a middle ground to have a decent enough detection with both satellites
    # lower_green: np.ndarray = np.array([55, 50, 100])  # Value is set to be within 40% and 80%
    # upper_green: np.ndarray = np.array([65, 255, 200])

    mask_green: MatLike = cv2.inRange(hsv_image, lower_green, upper_green)

    if DEBUG:
        cv2.imshow(f"{TEST_IMAGE} - Green Mask", mask_green)
        cv2.waitKey(0)

    # Eroding and dilating the image to clear noise
    kernel: np.ndarray = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    noise_cleared_image: MatLike = cv2.dilate(
        cv2.erode(
            mask_green,
            kernel,
            iterations=EROSION_DILATION_ITR),
        kernel,
        iterations=EROSION_DILATION_ITR)

    if DEBUG:
        cv2.imshow(f"{TEST_IMAGE} - Erosion & Dilation ({EROSION_DILATION_ITR} times, Kernel size: {KERNEL_SIZE})", noise_cleared_image)
        cv2.waitKey(0)

    # Dilating and eroding to fill gaps
    kernel: np.ndarray = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    gap_filled_image: MatLike = cv2.erode(
        cv2.dilate(
            noise_cleared_image,
            kernel,
            iterations=EROSION_DILATION_ITR),
        kernel,
        iterations=EROSION_DILATION_ITR)

    if DEBUG:
        cv2.imshow(f"{TEST_IMAGE} - Dilation & Erosion ({EROSION_DILATION_ITR} times, Kernel size: {KERNEL_SIZE})", gap_filled_image)
        cv2.waitKey(0)

    # Detecting the contours of the shapes in the image
    # https://www.geeksforgeeks.org/how-to-detect-shapes-in-images-in-python-using-opencv/
    contours_return: tuple[Sequence[MatLike], MatLike] = cv2.findContours(gap_filled_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours: Sequence[MatLike] = contours_return[0]
    i: int = 0
    for contour in contours:
        # here we are ignoring first counter because
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue

        cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)

        # finding center point of shape
        M: dict[str, float] = cv2.moments(contour)
        if M['m00'] != 0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

            cv2.putText(image, f"Center ({x},{y})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    if DEBUG:
        cv2.imshow(f"{TEST_IMAGE} Original Image - Contours Drawn", image)
        cv2.waitKey(0)

# white_pixel_coords: np.ndarray = np.argwhere(gap_filled_image != 0)
# structured_format: pd.DataFrame = pd.DataFrame([(y, x) for (x, y) in white_pixel_coords])
# structured_format = structured_format.rename(columns={0: "x_coord", 1: "y_coord"})
# structured_format.to_csv("./training_data/test.csv")
# if DEBUG:
#     print(structured_format)


if __name__ == "__main__":
    main()
