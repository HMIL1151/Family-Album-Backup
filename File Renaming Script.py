import os
import datetime
from PIL import Image
from mutagen.mp4 import MP4
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

# Get the folder path relative to the script's location
year = input("Year: ")
month = input("Month to Rename: ")
folder_path = f"D:\\Photos\\Ellie\\{year}\\{month}"

# Get a list of all files in the 'November' folder
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Get the total number of files to rename
total_files = len(files)

# Counter for files with no metadata
unknown_counter = 1

def get_media_creation_date(file_path):
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # For image files (JPEG, PNG, etc.)
            image = Image.open(file_path)
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    if tag == 36867:  # Exif tag for DateTimeOriginal
                        return datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        elif file_path.lower().endswith(('.mp4', '.mov', '.avi')):
            # For video files (MP4, MOV, AVI)
            video = MP4(file_path)
            if '©day' in video.tags:
                return datetime.datetime.strptime(video.tags['©day'], '%Y-%m-%d')
        elif file_path.lower().endswith(('.mp3', '.m4a')):
            # For audio files (MP3, M4A)
            audio = MP3(file_path, ID3=ID3)
            if audio.tags.get('TDRC'):
                return audio.tags['TDRC']
        return None
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return None

# Iterate over each file in the folder
for index, filename in enumerate(files, start=1):
    file_path = os.path.join(folder_path, filename)
    
    # Get the media creation date from metadata
    creation_date = get_media_creation_date(file_path)
    
    if creation_date:
        formatted_time = creation_date.strftime('%d-%m-%Y  %H.%M.%S')
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"{formatted_time}{file_extension}"
        new_file_path = os.path.join(folder_path, new_filename)

        # Check if the new filename already exists and make it unique if needed
        counter = 1
        while os.path.exists(new_file_path):
            new_filename = f"{formatted_time}_{counter}{file_extension}"
            new_file_path = os.path.join(folder_path, new_filename)
            counter += 1

        # Rename the file
        os.rename(file_path, new_file_path)
        
        # Print progress
        print(f"{index}/{total_files} renamed: {filename} -> {new_filename}")
    else:
        # Rename files with no metadata
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"Unknown Date {month} {year} #{unknown_counter}{file_extension}"
        new_file_path = os.path.join(folder_path, new_filename)
        
        # Ensure unique filename
        while os.path.exists(new_file_path):
            unknown_counter += 1
            new_filename = f"Unknown Date #{unknown_counter}{file_extension}"
            new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(file_path, new_file_path)
        
        # Increment the counter for unknown files
        unknown_counter += 1

        # Print progress
        print(f"{index}/{total_files} renamed: {filename} -> {new_filename}")
