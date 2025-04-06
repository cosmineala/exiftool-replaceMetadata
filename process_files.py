import os
import shutil
import subprocess
from pathlib import Path

def get_exiftool_path():
    return os.path.join('.', 'exiftool-13.26_64', 'exiftool(-k).exe')

def get_photo_dates(file_path):
    try:
        # Run exiftool to get photo dates and automatically send Enter
        cmd = [get_exiftool_path(), '-CreateDate', '-DateCreated', '-ModifyDate', '-s3', str(file_path)]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input='\n')
        
        dates = stdout.strip().split('\n')
        # Return the first non-empty date found
        for date in dates:
            if date.strip():
                return date.strip()
    except Exception as e:
        print(f"Error getting photo dates for {file_path}: {e}")
    return None

def set_file_dates(file_path, photo_date):
    try:
        # Run exiftool to set only file-related dates and automatically send Enter
        cmd = [
            get_exiftool_path(),
            f'-FileCreateDate={photo_date}',
            f'-FileModifyDate={photo_date}',
            f'-FileAccessDate={photo_date}',
            str(file_path)
        ]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.communicate(input='\n')
        return True
    except Exception as e:
        print(f"Error setting file dates for {file_path}: {e}")
        return False

def process_files(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all files from input folder
    input_path = Path(input_folder)
    files = [f for f in input_path.glob('*') if f.is_file()]
    
    for file_path in files:
        try:
            # Get the photo dates
            photo_date = get_photo_dates(file_path)
            
            # Create output file path
            output_file = Path(output_folder) / file_path.name
            
            # Copy file to output folder
            shutil.copy2(file_path, output_file)
            print(f"Copied {file_path.name} to output folder")
            
            # If we have photo date, update the file dates
            if photo_date:
                if set_file_dates(output_file, photo_date):
                    print(f"Updated file dates for {file_path.name} to {photo_date}")
                else:
                    print(f"Failed to update file dates for {file_path.name}")
            else:
                print(f"No photo date found for {file_path.name}, copied without modification")
                
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

if __name__ == "__main__":
    # Default folder paths
    input_folder = "inputData"
    output_folder = "outputData"
    
    print(f"Processing files from {input_folder} to {output_folder}")
    process_files(input_folder, output_folder)
    print("Processing complete!") 