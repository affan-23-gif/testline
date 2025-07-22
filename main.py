#Part 1: PDF Content Extraction, which includes:

#Extracting text from each page of the PDF

#Extracting and saving images from each page

#Creating a structured JSON file with text and image paths

import fitz  # PyMuPDF
import os
import json
from PIL import Image
from pathlib import Path

# Constants
INPUT_PDF = "data/input.pdf"
OUTPUT_FOLDER = "output"
IMAGES_FOLDER = os.path.join(OUTPUT_FOLDER, "images")
JSON_OUTPUT = os.path.join(OUTPUT_FOLDER, "content.json")

# Ensure folders exist
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# Updated function signature to accept `doc`
def extract_images_from_page(doc, page, page_number):
    images_info = []
    image_list = page.get_images(full=True)

    for img_index, img in enumerate(image_list, start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)  # ✅ Use doc instead of page.doc
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"page{page_number + 1}_img{img_index}.{image_ext}"
        image_path = os.path.join(IMAGES_FOLDER, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)

        images_info.append(image_path)

    return images_info

# Modified call inside extract_pdf_content
def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    content = []

    for page_number, page in enumerate(doc):
        text = page.get_text().strip()
        images = extract_images_from_page(doc, page, page_number)  # ✅ pass doc

        page_content = {
            "page_number": page_number + 1,
            "text": text,
            "images": images
        }

        content.append(page_content)

    return content

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    print("📄 Extracting content from PDF...")
    extracted_content = extract_pdf_content(INPUT_PDF)
    print(f"✅ Extracted content from {len(extracted_content)} pages.")

    print("💾 Saving content to JSON...")
    save_json(extracted_content, JSON_OUTPUT)
    print(f"✅ JSON saved at: {JSON_OUTPUT}")

if __name__ == "__main__":
    main()
