import cv2
import numpy as np

# from typing import Sequence
from cv2.typing import MatLike


DEBUG: bool = True
TEST_IMAGE: str = "test_images/20240223_Sentinel2_Hartbeespoort.png"
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
    # lower_green: np.ndarray = np.array([55, 50, 128])  # Value is set to 50%, because the BGR value of the green surface is 0, 128, 0
    # upper_green: np.ndarray = np.array([65, 255, 128])  # With a max value of 256, 128 is exactly this 50%

    # These thresholds are ideal for the Sentinel1 radar image
    # lower_green: np.ndarray = np.array([55, 50, 50])  # Value is set to be within 20% and 100%
    # upper_green: np.ndarray = np.array([65, 255, 255])

    # These thresholds are a middle ground to have a decent enough detection with both satellites
    lower_green: np.ndarray = np.array([55, 50, 100])  # Value is set to be within 40% and 80%
    upper_green: np.ndarray = np.array([65, 255, 200])

    mask_green: MatLike = cv2.inRange(hsv_image, lower_green, upper_green)

    if DEBUG:
        cv2.imshow(f"{TEST_IMAGE} - Green Mask", mask_green)
        cv2.waitKey(0)

    # Eroding and dilating the image to clear noise
    # kernel: np.ndarray = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
    # eroded_image: MatLike = cv2.erode(mask_green, kernel, iterations=EROSION_DILATION_ITR)
    # dilated_image: MatLike = cv2.dilate(eroded_image, kernel, iterations=EROSION_DILATION_ITR)

    # if DEBUG:
    #     cv2.imshow(f"{TEST_IMAGE} - Erosion & Dilation ({EROSION_DILATION_ITR} times, Kernel size: {KERNEL_SIZE})", dilated_image)
    #     cv2.waitKey(0)

    # Detecting the blob of the lake
    # detector: cv2.SimpleBlobDetector = cv2.SimpleBlobDetector().create()
    # keypoints: Sequence[cv2.KeyPoint] = detector.detect(image)
    # keypoint_image: MatLike = cv2.drawKeypoints(image, keypoints, np.array([]), (0, 0, 255), cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)

    # if DEBUG:
    #     cv2.imshow(f"{TEST_IMAGE} - Blob Detection", keypoint_image)
    #     cv2.waitKey(0)


if __name__ == "__main__":
    main()
