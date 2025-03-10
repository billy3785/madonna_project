import os
import glob

# Source directory (where your .txt files are located)
SOURCE_DIR = "/Users/billy/Desktop/webo_1958"

# Destination directory (where merged files will be saved)
DEST_DIR = "/Users/billy/Desktop/webo_1958_combined"
os.makedirs(DEST_DIR, exist_ok=True)

# Get all .txt files recursively
all_text_files = glob.glob(os.path.join(SOURCE_DIR, "**/*.txt"), recursive=True)

batch_size = 400  # Process 400 files per batch
batch_number = 1
file_counter = 0

# Create the first output file
output_file_path = os.path.join(DEST_DIR, f"combined_batch_{batch_number}.txt")
output_file = open(output_file_path, "w", encoding="utf-8")

for text_file in all_text_files:
    try:
        # Write the filename before its content
        output_file.write(f"\n--- FILE: {os.path.basename(text_file)} ---\n")
        
        with open(text_file, "r", encoding="utf-8") as f:
            output_file.write(f.read() + "\n\n")
        
        file_counter += 1

        # If we reach 400 files, close the current file and start a new batch
        if file_counter >= batch_size:
            output_file.close()
            batch_number += 1
            file_counter = 0
            output_file_path = os.path.join(DEST_DIR, f"combined_batch_{batch_number}.txt")
            output_file = open(output_file_path, "w", encoding="utf-8")

    except Exception as e:
        print(f"Error processing {text_file}: {e}")

# Close the last open file
output_file.close()

print(f"✅ Merging complete! Merged files are saved in {DEST_DIR}")