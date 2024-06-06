import subprocess
import json
import argparse
import os

def check_exiftool():
    """Check if exiftool is installed."""
    try:
        subprocess.run(['exiftool'], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        print("ExifTool is not installed. Please install ExifTool to use this program.")
        exit(1)

def get_metadata(image_path, include_all=False):
    try:
        result = subprocess.run(['exiftool', '-j', image_path], capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)
        if metadata:
            if include_all:
                return metadata[0]
            else:
                gps_data = {key: value for key, value in metadata[0].items() if key.startswith('GPS')}
                return gps_data
        else:
            print("No metadata found.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

def format_gps_data(gps_data):
    formatted_data = {}
    for key, value in gps_data.items():
        try:
            if key.endswith('Latitude') or key.endswith('Longitude'):
                # Check if the value is a properly formatted string
                parts = value.split(" ")
                if len(parts) == 3:
                    degrees, minutes, seconds = parts
                    formatted_data[key] = f"{degrees}°{minutes}'{seconds}\""
                else:
                    formatted_data[key] = value  # If it doesn't match the expected format, keep the original
            else:
                formatted_data[key] = value
        except Exception as e:
            print(f"Error formatting {key}: {value} - {e}")
            formatted_data[key] = value  # Keep the original value in case of error
    return formatted_data

def remove_gps_data(image_path):
    try:
        subprocess.run(['exiftool', '-gps:all=', '-overwrite_original', image_path], check=True)
        print(f"GPS data removed from {image_path}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while removing GPS data: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract GPS data from an image using exiftool.")
    parser.add_argument('image_path', type=str, help="Path to the image file")
    parser.add_argument('--all', action='store_true', help="Include all metadata, not just GPS data")
    parser.add_argument('--output', type=str, help="Path to save the output data")
    parser.add_argument('--format', choices=['json', 'csv', 'text'], default='text', help="Output format")
    parser.add_argument('--remove-gps', action='store_true', help="Remove GPS data from the image")
    args = parser.parse_args()

    if not os.path.isfile(args.image_path):
        print(f"File not found: {args.image_path}")
        return

    check_exiftool()

    if args.remove_gps:
        remove_gps_data(args.image_path)
        return

    metadata = get_metadata(args.image_path, include_all=args.all)
    if metadata:
        if args.all:
            data = metadata
        else:
            data = format_gps_data(metadata)

        if args.format == 'json':
            output_data = json.dumps(data, indent=4)
        elif args.format == 'csv':
            output_data = "Key,Value\n" + "\n".join([f"{key},{value}" for key, value in data.items()])
        else:
            output_data = "\n".join([f"{key}: {value}" for key, value in data.items()])

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_data)
            print(f"Output saved to {args.output}")
        else:
            print("Metadata:")
            print(output_data)
    else:
        print("No relevant data found.")

if __name__ == "__main__":
    main()
