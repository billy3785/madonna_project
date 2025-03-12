import os
import re
import json
import hashlib
import subprocess
from datetime import datetime

# Paths for raw input and processed output
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

# Dictionary for known projects (songs, albums, films, etc.)
PROJECTS = {
    "Holiday": {"type": "song", "album": "Madonna", "year": 1983},
    "Truth or Dare": {"type": "film", "role": "Self", "year": 1991},
    "MDNA": {"type": "album", "year": 2012},
}

# Set to track duplicate captions
seen_hashes = set()

### 🔹 DATE EXTRACTION ###
def normalize_date(text):
    """
    Convert descriptive dates into a standard format YYYY-MM-DD.
    Marks approximate dates with a flag.
    """
    date_patterns = [
        (r"(\d{4})", "%Y"),  # Year only
        (r"(\d{1,2}) (\w+) (\d{4})", "%d %B %Y"),  # Full date
        (r"(\w+) (\d{4})", "%B %Y"),  # Month & Year
        (r"(\w+)-(\w+) (\d{4})", "%B-%B %Y"),  # "March-April 1985"
    ]
    
    for pattern, date_format in date_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                normalized_date = datetime.strptime(match.group(0), date_format).strftime("%Y-%m-%d")
                approximate = "yes" if any(word in text.lower() for word in ["early", "late", "around"]) else "no"
                return {"normalized_date": normalized_date, "approximate": approximate}
            except ValueError:
                pass

    return {"normalized_date": None, "approximate": "unknown"}

### 🔹 LOCATION EXTRACTION ###
def extract_location(text):
    """
    Extracts structured location details: venue, city, state/country.
    """
    location_patterns = [
        r"at ([\w\s]+), ([\w\s]+), ([\w\s]+)",  # "at Madison Square Garden, New York, USA"
        r"in ([\w\s]+), ([\w\s]+)",  # "in Los Angeles, California"
        r"in ([\w\s]+)"  # "in Paris"
    ]
    for pattern in location_patterns:
        match = re.search(pattern, text)
        if match:
            return {
                "venue": match.group(1) if len(match.groups()) >= 1 else None,
                "city": match.group(2) if len(match.groups()) >= 2 else None,
                "state_or_country": match.group(3) if len(match.groups()) >= 3 else None
            }
    return None

### 🔹 PEOPLE EXTRACTION ###
def extract_people(text):
    """
    Identify people mentioned in text.
    Uses a basic list for now but will later use AI/NLP.
    """
    people = ["Madonna", "Ricardo Gomes", "Patrick Leonard"]
    found_people = [person for person in people if person in text]
    return found_people

### 🔹 PROJECT RECOGNITION ###
def match_project_references(text):
    """
    Finds known projects in text and maps them to structured data.
    """
    matched_projects = {name: details for name, details in PROJECTS.items() if name in text}
    return matched_projects

### 🔹 DUPLICATE DETECTION ###
def generate_text_hash(text):
    """
    Creates a hash of the text to detect duplicates.
    """
    return hashlib.md5(text.encode()).hexdigest()

def is_duplicate(text):
    """
    Checks if a text is a duplicate of previous entries.
    """
    text_hash = generate_text_hash(text)
    if text_hash in seen_hashes:
        return True
    seen_hashes.add(text_hash)
    return False

### 🔹 MEDIA FILE ASSOCIATION ###
def get_media_files(text_file_path):
    """
    Finds all media files in the same directory as the text file.
    """
    folder_path = os.path.dirname(text_file_path)
    media_extensions = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi"}
    media_files = [
        f for f in os.listdir(folder_path) 
        if os.path.splitext(f)[1].lower() in media_extensions
    ]
    return media_files

### 🔹 EMBED METADATA INTO MEDIA ###
def embed_metadata(media_path, metadata):
    """
    Writes structured metadata into media files using ExifTool.
    """
    exif_command = [
        "exiftool",
        f"-Description={metadata['original_text']}",
        f"-DateTimeOriginal={metadata['date']['normalized_date']}",
        f"-Keywords={','.join(metadata['people'])}",
        f"-Location={metadata['location']['city'] if metadata['location'] else ''}",
        media_path
    ]
    subprocess.run(exif_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

### 🔹 CLEAN & STRUCTURE TEXT FILES ###
def clean_text_file(file_path):
    """
    Reads a raw text file, extracts structured data, and saves it as JSON.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Check for duplicates
    if is_duplicate(raw_text):
        print(f"Skipping duplicate post: {file_path}")
        return

    # Extract metadata
    cleaned_data = {
        "original_filename": os.path.basename(file_path),
        "folder_path": os.path.dirname(file_path),
        "media_files": get_media_files(file_path),
        "original_text": raw_text.strip(),
        "date": normalize_date(raw_text),
        "location": extract_location(raw_text),
        "people": extract_people(raw_text),
        "projects": match_project_references(raw_text)
    }

    # Save structured data
    output_file = os.path.join(PROCESSED_DATA_DIR, os.path.basename(file_path).replace(".txt", ".json"))
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=4)

    # Embed metadata into associated media files
    for media_file in cleaned_data["media_files"]:
        media_path = os.path.join(cleaned_data["folder_path"], media_file)
        embed_metadata(media_path, cleaned_data)

    print(f"Processed: {file_path} → {output_file}")

### 🔹 PROCESS ALL FILES IN `data/raw` ###
def process_all_files():
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.makedirs(PROCESSED_DATA_DIR)

    for root, _, files in os.walk(RAW_DATA_DIR):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                clean_text_file(file_path)

if __name__ == "__main__":
    process_all_files()
    print("\n✅ Data cleaning complete! Check `data/processed/` for results.")