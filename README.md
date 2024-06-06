# Picturewho

A Python script to manage image metadata using `exiftool`. This script can extract GPS data, all metadata, save the extracted data in various formats, and remove GPS data from images.

## Requirements

- Python 3.12
- `exiftool`

## Usage

### Extract GPS Data Only

To extract GPS data from an image and display it in the terminal:
```sh
python picturewho.py /path/to/image.jpg
```

### Extract All Metadata

To extract all metadata from an image and display it in the terminal:
```sh
python picturewho.py /path/to/image.jpg --all
```

### Save Extracted GPS Data to a JSON File

To extract GPS data and save it to a JSON file:
```sh
python picturewho.py /path/to/image.jpg --output output.json --format json
```

### Save Extracted All Metadata to a CSV File

To extract all metadata and save it to a CSV file:
```sh
python picturewho.py /path/to/image.jpg --all --output output.csv --format csv
```

### Remove GPS Data from an Image

To remove GPS data from an image:
```sh
python picturewho.py /path/to/image.jpg --remove-gps
```

### Detailed Example Usage Scenarios

1. **Extract GPS Data and Display in JSON Format**
   ```sh
   python picturewho.py /path/to/image.jpg --format json
   ```

2. **Extract All Metadata and Save to a Text File**
   ```sh
   python picturewho.py /path/to/image.jpg --all --output metadata.txt --format text
   ```

3. **Remove GPS Data and then Extract Remaining Metadata**
   ```sh
   python picturewho.py /path/to/image.jpg --remove-gps
   python picturewho.py /path/to/image.jpg --all --output metadata_after_removal.txt --format text
   ```

## Arguments

- `image_path`: Path to the image file.
- `--all`: Include all metadata, not just GPS data.
- `--output`: Path to save the output data.
- `--format`: Output format (`json`, `csv`, `text`). Default is `text`.
- `--remove-gps`: Remove GPS data from the image.

## License

This project is licensed under Creative Commons Zero. Happy Coding!
