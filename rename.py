from PIL import Image
import sys
import os
import datetime
import piexif
import re
import time

# Set list of valid file extensions
valid_extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

# If folder path argument exists then use it
# Else use the current running folder
if len(sys.argv) > 1:
    folder_path = sys.argv[1]
else:
    folder_path = os.getcwd()

# Get all files from folder
file_names = os.listdir(folder_path)

print("processing: " + folder_path)

# For each file
for file_name in file_names:

    # Get the file extension
    file_ext = os.path.splitext(file_name)[1]

    # If the file does not have a valid file extension
    # then skip it
    if (file_ext not in valid_extensions):
        continue

    # Create the old file path
    old_file_path = os.path.join(folder_path, file_name)

    # Open the image
    image = Image.open(old_file_path)

    # Get the date taken from EXIF metadata
    try:
        date_taken = image._getexif()[36867]
    except:
        date_modified = os.path.getmtime(old_file_path)
        # get the readable timestamp format
        format_time = datetime.datetime.fromtimestamp(date_modified)

        # convert time into string
        date_taken = format_time.strftime(
            "%Y:%m:%d %H:%M:%S")  # same format as _getexif()[36867] 2015:01:01 09:00:00

    # Close the image
    image.close()

    match = re.match(r"^(\d+):(\d+):(\d+) (\d+):(\d+):(\d+)", date_taken)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    hour = match.group(4)
    minute = match.group(5)
    second = match.group(6)

    try:
        if file_ext in [".png", ".PNG"]:
            date = datetime.datetime(
                year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))
            modTime = time.mktime(date.timetuple())
            os.utime(old_file_path, (modTime, modTime))

        else:
            exif_dict = piexif.load(old_file_path)
            # Update DateTimeOriginal
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_taken
            # Update DateTimeDigitized
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_taken
            # Update DateTime
            exif_dict['0th'][piexif.ImageIFD.DateTime] = date_taken
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, old_file_path)
    except Exception as e:
        print(file_name + ":" + e)

    # Reformat the date taken to "YYYYMMDD-HHmmss"
    date_time = date_taken \
        .replace(":", "")      \
        .replace(" ", "-")

    # Combine the new file name and file extension
    new_file_name = date_time + file_ext

    id = 1
    while os.path.exists(os.path.join(folder_path, new_file_name)):
        new_file_name = date_time + "_" + str(id) + file_ext
        id += 1

    # Create the new folder path
    new_file_path = os.path.join(folder_path, new_file_name)

    # Rename the file
    os.rename(old_file_path, new_file_path)
