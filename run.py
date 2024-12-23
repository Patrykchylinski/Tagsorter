from typing import Generator, Iterable
from tagger.interrogator import WaifuDiffusionInterrogator
from PIL import Image
from pathlib import Path
import sys
import os
import shutil
import psutil

# Single model configuration
MODEL = WaifuDiffusionInterrogator(
    'WD14 ViT v3',
    repo_id='SmilingWolf/wd-vit-tagger-v3'
)

def get_input_path() -> Path:
    while True:
        path = input("Enter path to images: ").strip()
        if not path:
            print("Path cannot be empty!")
            continue
        
        path = Path(path)
        if not path.exists():
            print("Path does not exist!")
            continue
            
        return path

def get_operation_mode() -> tuple[str, Path | None]:
    while True:
        print("\nChoose operation:")
        print("1. Delete files")
        print("2. Copy files")
        print("3. Move files")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            return "delete", None
        elif choice in ["2", "3"]:
            while True:
                dest = input("Enter destination path: ").strip()
                if not dest:
                    print("Path cannot be empty!")
                    continue
                
                dest_path = Path(dest)
                if not dest_path.exists():
                    try:
                        dest_path.mkdir(parents=True)
                        print(f"Created directory: {dest_path}")
                    except Exception as e:
                        print(f"Error creating directory: {e}")
                        continue
                
                return "copy" if choice == "2" else "move", dest_path
        else:
            print("Invalid choice! Please enter 1, 2, or 3")

def get_tags() -> list[str]:
    while True:
        tags = input("\nEnter tags (comma separated): ").strip()
        if not tags:
            print("Please enter at least one tag!")
            continue
        
        return [tag.strip() for tag in tags.split(",") if tag.strip()]

def show_resource_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    cpu_percent = process.cpu_percent()
    print(f"\nResource usage:")
    print(f"Memory: {memory_usage:.1f} MB")
    print(f"CPU: {cpu_percent}%")

def process_images(source_path: Path, operation: str, dest_path: Path | None, search_tags: list[str]):
    # Initialize model
    print("Loading AI model (WD14 ViT v3)...")
    show_resource_usage()
    
    # Use single model
    interrogator = MODEL
    
    print("\nModel loaded!")
    show_resource_usage()
    
    # Get all image files
    image_files = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp'):
        image_files.extend(source_path.glob(ext))
    
    if not image_files:
        print("No image files found!")
        return
    
    total = len(image_files)
    print(f"\nFound {total} images")
    print("Processing...")
    
    processed = 0
    matched = 0
    
    for img_path in image_files:
        try:
            if processed % 10 == 0:  # pokazuj zużycie co 10 obrazów
                show_resource_usage()
                
            # Open and analyze image
            img = Image.open(img_path)
            _, tags = interrogator.interrogate(img)
            
            # Filter tags by confidence threshold
            image_tags = {k.lower(): v for k, v in tags.items() if v >= 0.5}
            
            # Check for matching tags
            has_match = any(search_tag.lower() in image_tags for search_tag in search_tags)
            
            processed += 1
            
            if has_match:
                matched += 1
                if operation == "delete":
                    os.remove(img_path)
                elif operation == "copy":
                    shutil.copy2(img_path, dest_path / img_path.name)
                else:  # move
                    shutil.move(img_path, dest_path / img_path.name)
                print(f"\r{processed}/{total} - Found match! ({matched} matches so far)", end="")
            else:
                print(f"\r{processed}/{total} - Processing...", end="")
            
        except Exception as e:
            print(f"\nError processing {img_path}: {e}")
            continue

    print(f"\n\nComplete! Found {matched} matches in {processed} images")
    if matched > 0:
        if operation == "delete":
            print(f"Deleted {matched} files")
        elif operation == "copy":
            print(f"Copied {matched} files to {dest_path}")
        else:
            print(f"Moved {matched} files to {dest_path}")

    print("\nProcessing complete!")
    show_resource_usage()

def main():
    print("TagSorter\n")
    
    # Get source path
    source_path = get_input_path()
    
    # Get operation mode and destination path
    operation, dest_path = get_operation_mode()
    
    # Get tags to search for
    search_tags = get_tags()
    
    # Process images
    process_images(source_path, operation, dest_path, search_tags)

if __name__ == "__main__":
    main()


