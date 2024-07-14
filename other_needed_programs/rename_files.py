import os

# Mapping of old names to new names based on CARD_VALUES
old_to_new_names = {
    'ace': 'A', 'two': '2', 'three': '3', 'four': '4', 
    'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 
    'nine': '9', 'ten': '10', 'jack': 'J', 'queen': 'Q', 'king': 'K'
}

def rename_files(directory):
    # Walk through all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a .jpg file
            if file.endswith('.jpg'):
                # Get the base name without .jpg
                base_name = file[:-4]
                if base_name in old_to_new_names:
                    # Construct the new file name
                    new_name = f"{old_to_new_names[base_name]}.jpg"
                    # Full path for old and new file names
                    old_file = os.path.join(root, file)
                    new_file = os.path.join(root, new_name)
                    # Rename the file
                    os.rename(old_file, new_file)
                    print(f'Renamed {old_file} to {new_file}')

# Provide the path to the folder containing the subfolders
root_folder = './sprites'
rename_files(root_folder)
