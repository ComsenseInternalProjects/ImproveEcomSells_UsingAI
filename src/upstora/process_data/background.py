import cv2
import numpy as np
from collections import Counter
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import logging

# Configure logging to print messages to console
logging.basicConfig(filename='scraper_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def image_size(url):
    try:
        # Download the image
        response = requests.get(url)
        img_data = BytesIO(response.content)

        img = Image.open(img_data)
        width, height = img.size
        return width, height
    except Exception as e:
        logging.error(f"Error in image_size: {e}")
        return None, None

class BackgroundColorDetector():
    def __init__(self, image_url):
        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                raise ValueError(f"Error: Unable to download the image from {image_url}")

            image_bytes = BytesIO(response.content)
            self.img = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), 1)

            if self.img is None:
                raise ValueError(f"Error: Unable to decode the image from {image_url}")

            self.manual_count = {}
            self.w, self.h, self.channels = self.img.shape
            self.total_pixels = self.w * self.h
            self.number_counter = None
        except Exception as e:
            logging.error(f"Error in BackgroundColorDetector initialization: {e}")

    def count(self):
        try:
            self.number_counter = Counter()
            for y in range(0, self.h):
                for x in range(0, self.w):
                    RGB = (self.img[x, y, 2], self.img[x, y, 1], self.img[x, y, 0])
                    self.number_counter[RGB] += 1
        except Exception as e:
            logging.error(f"Error in count method: {e}")

    def average_colour(self):
        try:
            if self.number_counter:
                sample = min(10, len(self.number_counter))
                if sample > 0:
                    red, green, blue = 0, 0, 0
                    for top in range(sample):
                        red += self.number_counter[top][0][0]
                        green += self.number_counter[top][0][1]
                        blue += self.number_counter[top][0][2]

                    average_red = round(red / sample)
                    average_green = round(green / sample)
                    average_blue = round(blue / sample)
                    return average_red, average_green, average_blue
                else:
                    logging.warning("No top colors found to calculate an average.")
            else:
                logging.warning("No color data available to calculate an average.")
        except Exception as e:
            logging.error(f"Error in average_colour method: {e}")
        return None

    def twenty_most_common(self):
        try:
            self.count()
            self.number_counter = Counter(self.number_counter).most_common(20)
            for rgb, value in self.number_counter:
                return rgb, value, ((float(value) / self.total_pixels) * 100)
        except Exception as e:
            logging.error(f"Error in twenty_most_common method: {e}")
        return None

    def detect(self):
        try:
            self.twenty_most_common()
            self.percentage_of_first = (
                float(self.number_counter[0][1]) / self.total_pixels)
            if self.percentage_of_first > 0.5:
                return self.number_counter[0][0]
            else:
                return self.average_colour()
        except Exception as e:
            logging.error(f"Error in detect method: {e}")
            return None

def is_white_or_near_white(rgb, threshold):
    try:
        reference_white = (255, 255, 255)
        distance = sum((a - b) ** 2 for a, b in zip(rgb, reference_white)) ** 0.5
        if distance <= threshold:
            return "Background is white or nearly white"
        else:
            return "Background is not white"
    except Exception as e:
        logging.error(f"Error in is_white_or_near_white function: {e}")
        return None

def image_insight(url):
    try:
        image_path = url
        detector = BackgroundColorDetector(image_path)
        rgb = detector.detect()
        if rgb is not None:
            result_is_white = is_white_or_near_white(rgb, 35)

            # Get the result from image_size function
            width, height = image_size(image_path)
            df = pd.DataFrame({
                'background': [result_is_white],
                'Image_Width': [width],
                'Image_Height': [height]
            })
            return df
        else:
            logging.warning("Unable to obtain RGB values.")
            return None
    except Exception as e:
        logging.error(f"Error in image_insight function: {e}")
        return None

if __name__ == "__main__":
    image_path = "https://m.media-amazon.com/images/I/71AcSKuUFIL._AC_SX679_.jpg"
    df = image_insight(image_path)
    if df is not None:
        print(df)
