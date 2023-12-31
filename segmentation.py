import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation


# For webcam input:
BG_COLOR = (192, 192, 192) # gray
cap = cv2.VideoCapture(0)
with mp_selfie_segmentation.SelfieSegmentation(
    model_selection=1) as selfie_segmentation:
  bg_image = None
  while cap.isOpened():
    success, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = selfie_segmentation.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    # The background can be customized.
    #   a) Load an image (with the same width and height of the input image) to
    #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
    #   b) Blur the input image by applying image filtering, e.g.,
    #      bg_image = cv2.GaussianBlur(image,(55,55),0)
    if bg_image is None:
      bg_image = np.zeros(image.shape, dtype=np.uint8)
      #bg_image = cv2.imread("G:\Rajarshi\Code\python\Pic.jpg")
      #bg_image[:] = BG_COLOR
      #bg_image = image
      bg_image = cv2.GaussianBlur(bg_image,(5,5),0)

    k = cv2.waitKey(1)
    if k == ord("t"):
      bg_image = np.where(condition, image, bg_image)
      print("ok")
    elif k == ord("o"):
      cv2.imwrite("picture.jpg",bg_image)
      break
    elif k == ord("q"):
      print("DONE!")
      break

    output_image = np.where(condition, image, bg_image)

    cv2.imshow('MediaPipe Selfie Segmentation', output_image)
cap.release()