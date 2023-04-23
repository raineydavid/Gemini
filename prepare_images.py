import zipfile
from transformers import pipeline
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from tqdm import tqdm
import exifread
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class ImageInfoExtractor:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
        self.base_image_dir = 'images'
        self.image_dir = None  # This will be set in extract_images method

    def extract_images(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            # Extract the images into a subdirectory with the same name as the ZIP file (without the .zip extension)
            extract_dir = os.path.splitext(os.path.basename(self.zip_path))[0]
            zip_ref.extractall(os.path.join(self.base_image_dir, extract_dir))
            self.image_dir = os.path.join(self.base_image_dir, extract_dir)

    def get_exif_data(self, image_path):
        image = Image.open(image_path)
        exif_data = image._getexif()
        return {TAGS[k]: v for k, v in exif_data.items() if k in TAGS}

    def decimal_degrees(self, deg, min, sec):
        return deg + min / 60 + sec / 3600

    def get_location_description(self, latitude, longitude):
        geolocator = Nominatim(user_agent="geoapiExercises")
        try:
            location = geolocator.reverse(f"{latitude}, {longitude}")
            return location.address
        except GeocoderTimedOut:
            return "Geocoder timed out. Please try again."

    def get_location_and_datetime(self, exif_data):
        def dms_to_dd(d, m, s):
            return d + m / 60.0 + s / 3600.0

        location = None
        datetime_taken = None

        if 'GPSInfo' in exif_data:
            gps_info = exif_data['GPSInfo']
            if 1 in gps_info and 2 in gps_info and 3 in gps_info and 4 in gps_info:
                lat_dms = gps_info[2]
                lon_dms = gps_info[4]
                lat_ref = gps_info[1]
                lon_ref = gps_info[3]
                latitude = dms_to_dd(lat_dms[0], lat_dms[1], lat_dms[2])
                longitude = dms_to_dd(lon_dms[0], lon_dms[1], lon_dms[2])
                if lat_ref == 'S':
                    latitude = -latitude
                if lon_ref == 'W':
                    longitude = -longitude
                location = self.get_location_description(latitude, longitude)
        if 'DateTime' in exif_data:
            datetime_taken = exif_data['DateTime']
        return location, datetime_taken

    def extract_image_info(self):
        self.extract_images()
        image_info = {}
        for file_name in tqdm(os.listdir(self.image_dir)):
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension in ['.png', '.jpg', '.jpeg']:
                image_path = os.path.join(self.image_dir, file_name)
                image = Image.open(image_path)
                    
                # Get the EXIF data for the image
                exif_data = self.get_exif_data(image_path)
                
                # Use the EXIF data to extract location and datetime information
                location, datetime_taken = self.get_location_and_datetime(exif_data)
                
                caption = self.image_to_text(image)[0]["generated_text"]
                image_data = {
                    "caption": caption,
                    "date_taken": datetime_taken,
                    "location": location
                }
                image_info[file_name] = image_data
        
        return image_info


import utils as u
import json

zip_path = 'images.zip'
extractor = ImageInfoExtractor(zip_path)
image_info = extractor.extract_image_info()

# Convert the image_info to a serializable format
serializable_image_info = u.convert_to_serializable(image_info)

# Serialize the data to JSON
json_data = json.dumps(serializable_image_info)

# Write the JSON data to a file
with open('image_info.json', 'w') as outfile:
    outfile.write(json_data)

## goal, embed an entire date essentially into a single "memory"