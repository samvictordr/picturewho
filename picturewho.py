import subprocess
import json
import argparse

def get_gps_data(image_path):
    try:
        result = subprocess.run(['exiftool', '-j', image_path], capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)
        if metadata:
            gps_data = {}
            for key in metadata[0]:
                if key.startswith('GPS'):
                    gps_data[key] = metadata[0][key]
            return gps_data
        else:
            print("No metadata found.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Extract GPS data from an image using exiftool.")
    parser.add_argument('image_path', type=str, help="Path to the image file")
    args = parser.parse_args()

    gps_data = get_gps_data(args.image_path)
    if gps_data:
        print("GPS Data:")
        for key, value in gps_data.items():
            print(f"{key}: {value}")
    else:
        print("No GPS data found.")

if __name__ == "__main__":
    main()

