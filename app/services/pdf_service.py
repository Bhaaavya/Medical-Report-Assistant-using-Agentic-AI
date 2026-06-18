import fitz


def calculate_extraction_quality(text: str, page_count: int):
    if not text or len(text.strip()) < 100:
        return "poor", True

    score = 0

    if len(text) > 500:
        score += 2

    medical_keywords = [
        "hemoglobin", "wbc", "rbc", "platelet", "glucose",
        "cholesterol", "creatinine", "urea", "sodium",
        "potassium", "impression", "diagnosis", "medication",
        "dosage", "reference", "range"
    ]

    lower_text = text.lower()

    keyword_count = sum(1 for word in medical_keywords if word in lower_text)

    if keyword_count >= 3:
        score += 2

    digit_count = sum(1 for char in text if char.isdigit())

    if digit_count >= 20:
        score += 2

    weird_chars = sum(1 for char in text if not char.isprintable())

    weird_ratio = weird_chars / max(len(text), 1)

    if weird_ratio < 0.05:
        score += 2

    avg_chars_per_page = len(text) / max(page_count, 1)

    if avg_chars_per_page > 300:
        score += 2

    if score >= 7:
        return "good", False

    if score >= 4:
        return "medium", False

    return "poor", True


def extract_with_docling(file_path: str):
    try:
        from docling.document_converter import DocumentConverter

        converter = DocumentConverter()
        result = converter.convert(str(file_path))

        text = result.document.export_to_markdown()

        return text, "docling"

    except Exception:
        return "", "docling_failed"
    
    
    
        
def extract_with_pymupdf(file_path: str):
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()
        text += "\n"

    page_count = document.page_count

    document.close()

    return text, page_count


def extract_report_content(file_path: str):
    text, method = extract_with_docling(file_path)

    page_count = None

    if text and len(text.strip()) > 100:
        try:
            doc = fitz.open(file_path)
            page_count = doc.page_count
            doc.close()
        except Exception:
            page_count = None

        quality, needs_ocr = calculate_extraction_quality(
            text=text,
            page_count=page_count or 1
        )

        return {
            "raw_text": text,
            "extraction_method": method,
            "extraction_quality": quality,
            "page_count": page_count,
            "needs_ocr": needs_ocr
        }

    fallback_text, page_count = extract_with_pymupdf(file_path)

    quality, needs_ocr = calculate_extraction_quality(
        text=fallback_text,
        page_count=page_count
    )

    return {
        "raw_text": fallback_text,
        "extraction_method": "pymupdf_fallback",
        "extraction_quality": quality,
        "page_count": page_count,
        "needs_ocr": needs_ocr
    }