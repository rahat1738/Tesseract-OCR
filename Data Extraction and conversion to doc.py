import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm
import multiprocessing
import os
import time
import locale
from docx import Document  # For saving to Word

# === PATH SETTINGS ===
pytesseract.pytesseract.tesseract_cmd = r"D:\\Software\\Tesseract\\tesseract.exe" #download tesseract and provide the file path here
pdf_path = r"C:\\Users\\Nuruzzaman Rahat\\Downloads\\Income Tax law 2023.pdf" # set the path of your file from which you one to extract text
docx_path = r"C:\\Users\\Nuruzzaman Rahat\\Downloads\\income_tax_law_plain.docx"
poppler_path = r"D:\\Software\\poppler-24.08.0\\Library\\bin"

def ocr_page(page_image):
    """Perform OCR on a single page (Bengali + English)."""
    try:
        custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
        text = pytesseract.image_to_string(
            page_image,
            lang='ben+eng',
            config=custom_config
        )
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='ignore')
        return text.strip()
    except Exception as e:
        print(f"Error processing a page: {e}")
        return ""

def main():
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass
    
    total_start_time = time.time()

    # Detect CPU cores
    try:
        num_cores = multiprocessing.cpu_count()
    except NotImplementedError:
        num_cores = 4
        
    print(f"Using {num_cores} cores for OCR.")

    # Check Bengali support
    try:
        available_langs = pytesseract.get_languages()
        if 'ben' not in available_langs:
            print("WARNING: Bengali language pack not found in Tesseract!")
            return
    except Exception as e:
        print(f"Warning: Could not check Tesseract languages: {e}")

    # Step 1: Convert PDF to images
    print("\n[Step 1] Converting PDF pages to images...")
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found at {pdf_path}")
        return
        
    try:
        pages = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=poppler_path,
            thread_count=num_cores
        )
        print(f"Converted {len(pages)} pages.")
    except Exception as e:
        print(f"ERROR converting PDF: {e}")
        return

    # Step 2: OCR
    print("\n[Step 2] Performing OCR...")
    page_texts = []
    with multiprocessing.Pool(processes=num_cores) as pool:
        for text in tqdm(pool.imap(ocr_page, pages), total=len(pages), desc="OCR Progress", unit="page"):
            page_texts.append(text)

    # Step 3: Save to DOCX
    print("\n[Step 3] Writing to Word file...")
    document = Document()
    for page_num, text in enumerate(page_texts, start=1):
        document.add_paragraph(text)
        document.add_page_break()  # Keep page separation
    
    document.save(docx_path)
    total_duration = time.time() - total_start_time

    print(f"\n✅ OCR complete. Plain text Word file saved at: {docx_path}")
    print(f"Total execution time: {total_duration:.2f} seconds.")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

