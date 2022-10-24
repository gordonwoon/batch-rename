from PIL import Image
import sys
import os
import datetime

# Set list of valid file extensions
valid_extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

# If folder path argument exists then use it
# Else use the current running folder
if len(sys.argv) < 1:
    folder_path = sys.argv[1]
else:
    folder_path = os.getcwd()

# Get all files from folder
file_names = os.listdir(folder_path)

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
