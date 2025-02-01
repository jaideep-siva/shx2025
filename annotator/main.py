import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from annotator import Annotator

class AnomalyAnnotatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anomaly Annotator")
        self.image_dir = ""
        self.image_list = []
        self.current_image_index = 0
        self.current_image = None  # Keep a reference to avoid garbage collection

        # Create a new directory for annotations
        self.annotation_dir = os.path.join(os.getcwd(), "annotations")
        os.makedirs(self.annotation_dir, exist_ok=True)

        # GUI Elements
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.btn_load = tk.Button(root, text="Load Directory", command=self.load_directory)
        self.btn_load.pack(side=tk.LEFT)

        self.btn_no_anomaly = tk.Button(root, text="No Anomaly", command=self.mark_no_anomaly)
        self.btn_no_anomaly.pack(side=tk.LEFT)

        self.btn_segment = tk.Button(root, text="Segment Anomaly", command=self.segment_anomaly)
        self.btn_segment.pack(side=tk.LEFT)

        self.btn_prev = tk.Button(root, text="Previous Image", command=self.prev_image)
        self.btn_prev.pack(side=tk.RIGHT)

        self.btn_next = tk.Button(root, text="Next Image", command=self.next_image)
        self.btn_next.pack(side=tk.RIGHT)

        # Counter for processed images
        self.counter_label = tk.Label(root, text="Processed: 0 / Remaining: 0")
        self.counter_label.pack(side=tk.BOTTOM)

    def load_directory(self):
        self.image_dir = filedialog.askdirectory()
        if self.image_dir:
            self.image_list = [
                os.path.join(self.image_dir, f) 
                for f in os.listdir(self.image_dir) 
                if f.endswith(('.png', '.jpg', '.jpeg'))
            ]
            print(f"Loaded {len(self.image_list)} images from {self.image_dir}")  # Debug
            if self.image_list:
                self.current_image_index = 0
                self.update_counter()
                self.show_image()
            else:
                print("No valid images found in the directory.")  # Debug

    def show_image(self):
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            print(f"Loading image: {image_path}")  # Debug

            # Load image using OpenCV
            self.current_image_cv = cv2.imread(image_path)
            if self.current_image_cv is None:
                print(f"Failed to load image: {image_path}")  # Debug
                return

            # Convert OpenCV image (BGR) to RGB for PIL
            self.current_image_cv = cv2.cvtColor(self.current_image_cv, cv2.COLOR_BGR2RGB)
            self.current_image_pil = Image.fromarray(self.current_image_cv)
            self.current_image_tk = ImageTk.PhotoImage(self.current_image_pil)

            # Display image on canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image_tk)
        else:
            print("No images to display.")  # Debug

    def mark_no_anomaly(self):
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            print(f"Marking as no anomaly: {image_path}")  # Debug

            # Create 'no_anomaly' directory inside 'annotations'
            no_anomaly_dir = os.path.join(self.annotation_dir, "no_anomaly")
            os.makedirs(no_anomaly_dir, exist_ok=True)

            # Copy the image to the 'no_anomaly' directory
            destination_path = os.path.join(no_anomaly_dir, os.path.basename(image_path))
            try:
                import shutil
                shutil.copy(image_path, destination_path)
                print(f"Copied {image_path} to {destination_path}")
                messagebox.showinfo("Success", "Image marked as 'No Anomaly' and saved.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

            # Move to the next image
            self.next_image()

    def segment_anomaly(self):
        if self.image_list:
            image_path = self.image_list[self.current_image_index]
            print(f"Segmenting anomaly: {image_path}")  # Debug

            # Create 'anomaly' directory inside 'annotations'
            anomaly_dir = os.path.join(self.annotation_dir, "anomaly")
            os.makedirs(anomaly_dir, exist_ok=True)

            # Pass the anomaly directory to the annotator
            annotator = Annotator(image_path, anomaly_dir)
            annotator.segment_anomaly()

            # Show confirmation dialog
            if annotator.annotation_saved:
                messagebox.showinfo("Success", "Anomaly annotation saved.")
            else:
                messagebox.showinfo("Canceled", "Anomaly annotation canceled.")

            # Move to the next image
            self.next_image()

    def next_image(self):
        if self.current_image_index < len(self.image_list) - 1:
            self.current_image_index += 1
            self.update_counter()
            self.show_image()
        else:
            print("Reached the end of the image list.")  # Debug

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_counter()
            self.show_image()
        else:
            print("Reached the beginning of the image list.")  # Debug

    def update_counter(self):
        processed = self.current_image_index
        remaining = len(self.image_list) - processed - 1
        self.counter_label.config(text=f"Processed: {processed} / Remaining: {remaining}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnomalyAnnotatorApp(root)
    root.mainloop()