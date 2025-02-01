import cv2
import numpy as np
import os

class Annotator:
    def __init__(self, image_path, output_dir):
        self.image_path = image_path
        self.output_dir = output_dir
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        self.mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        self.brush_size = 5  # Default brush size
        self.drawing = False  # To track if the mouse is being pressed
        self.clone = self.image.copy()  # Clone of the original image for resetting
        self.annotation_saved = False  # Flag to track if annotation was saved

    def segment_anomaly(self):
        # Create a window for segmentation
        cv2.namedWindow("Segment Anomaly")
        cv2.createTrackbar("Brush Size", "Segment Anomaly", self.brush_size, 50, self.update_brush_size)

        # Mouse callback function
        def draw_mask(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                cv2.circle(self.mask, (x, y), self.brush_size, 255, -1)
                cv2.circle(self.image, (x, y), self.brush_size, (0, 255, 0), -1)
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing:
                    cv2.circle(self.mask, (x, y), self.brush_size, 255, -1)
                    cv2.circle(self.image, (x, y), self.brush_size, (0, 255, 0), -1)
            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False

        cv2.setMouseCallback("Segment Anomaly", draw_mask)

        while True:
            # Display the image
            cv2.imshow("Segment Anomaly", self.image)

            # Add instructions for confirmation
            cv2.displayOverlay("Segment Anomaly", "Press 'Enter' to confirm, 'ESC' to cancel, 'R' to reset", 1000)

            # Wait for key press
            key = cv2.waitKey(1) & 0xFF

            # Exit on ESC key
            if key == 27:  # ESC key
                print("Annotation canceled.")
                break

            # Confirm annotation on Enter key
            if key == 13:  # Enter key
                self.save_annotation()
                self.annotation_saved = True
                print("Annotation confirmed and saved.")
                break

            # Reset drawing on 'R' key
            if key == ord('r'):
                self.image = self.clone.copy()
                self.mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
                print("Drawing reset.")

        cv2.destroyAllWindows()

    def update_brush_size(self, value):
        self.brush_size = value

    def save_annotation(self):
        # Save the annotated image and mask
        os.makedirs(self.output_dir, exist_ok=True)
        cv2.imwrite(os.path.join(self.output_dir, os.path.basename(self.image_path)), self.image)
        cv2.imwrite(os.path.join(self.output_dir, "mask_" + os.path.basename(self.image_path)), self.mask)
        print(f"Annotation saved in {self.output_dir}")