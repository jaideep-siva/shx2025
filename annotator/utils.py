# annotator.py
import cv2
import numpy as np

class Annotator:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.mask = np.zeros(self.image.shape[:2], dtype=np.uint8)

    def segment_anomaly(self):
        # Use OpenCV to allow user to draw on the image
        def draw_mask(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.circle(self.mask, (x, y), 5, 255, -1)
                cv2.circle(self.image, (x, y), 5, (0, 255, 0), -1)

        cv2.namedWindow("Segment Anomaly")
        cv2.setMouseCallback("Segment Anomaly", draw_mask)

        while True:
            cv2.imshow("Segment Anomaly", self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Press ESC to exit
                break

        cv2.destroyAllWindows()

        # Save the annotated image and mask
        os.makedirs("anomaly", exist_ok=True)
        cv2.imwrite(os.path.join("anomaly", os.path.basename(self.image_path)), self.image)
        cv2.imwrite(os.path.join("anomaly", "mask_" + os.path.basename(self.image_path)), self.mask)