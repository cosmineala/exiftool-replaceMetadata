import os
import subprocess
from pathlib import Path

def get_exiftool_path():
    return os.path.join('.', 'exiftool-13.26_64', 'exiftool(-k).exe')

def check_file_metadata(file_path):
    try:
        # Run exiftool to get all metadata
        cmd = [get_exiftool_path(), str(file_path)]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input='\n')
        return stdout
    except Exception as e:
        print(f"Error checking metadata for {file_path}: {e}")
        return None

def main():
    output_folder = "outputData"
    output_path = Path(output_folder)
    
    if not output_path.exists():
        print(f"Output folder {output_folder} does not exist!")
        return
    
    # Get first 5 files from output folder
    files = [f for f in output_path.glob('*') if f.is_file()][:5]
    
    if not files:
        print(f"No files found in {output_folder}")
        return
    
    print(f"Checking metadata for first {len(files)} files in {output_folder}")
    print("\n" + "="*80)
    
    for file_path in files:
        print(f"\nFile: {file_path.name}")
        print("#"*80)
        metadata = check_file_metadata(file_path)
        if metadata:
            print(metadata)
        print("#"*80 + "\n")

if __name__ == "__main__":
    main() 