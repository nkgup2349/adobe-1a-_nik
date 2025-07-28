# import os
# import fitz  # PyMuPDF
# import json

# def is_heading(text, font_size, font_name):
#     if font_size > 15 and "Bold" in font_name:
#         return "H1"
#     elif font_size > 13:
#         return "H2"
#     elif font_size > 11:
#         return "H3"
#     return None

# def extract_title_from_first_page(doc):
#     first_page = doc[0]
#     blocks = first_page.get_text("dict")["blocks"]

#     title_candidate = ""
#     max_size = 0

#     for block in blocks:
#         for line in block.get("lines", []):
#             text = " ".join(span["text"].strip() for span in line["spans"]).strip()
#             if not text or len(text.split()) < 2:
#                 continue
#             span = line["spans"][0]
#             size = span["size"]
#             font = span["font"]
#             is_bold = "Bold" in font or "bold" in font.lower()

#             if not is_bold:
#                 continue

#             if any(text.lower().startswith(prefix) for prefix in (
#                 "table of contents", "revision history", "1.", "2.", "overview"
#             )):
#                 continue

#             if size > max_size:
#                 max_size = size
#                 title_candidate = text

#     return title_candidate or doc.metadata.get("title") or "Untitled"

# def extract_outline_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     outline = []
#     title = extract_title_from_first_page(doc)

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         blocks = page.get_text("dict")["blocks"]
#         for block in blocks:
#             for line in block.get("lines", []):
#                 for span in line.get("spans", []):
#                     text = span["text"].strip()
#                     if len(text) < 3:
#                         continue
#                     if text == title:
#                         continue  # Skip title from outline
#                     heading_level = is_heading(text, span["size"], span["font"])
#                     if heading_level:
#                         outline.append({
#                             "level": heading_level,
#                             "text": text,
#                             "page": page_num + 1
#                         })

#     return {
#         "title": title,
#         "outline": outline
#     }

# def process_all_pdfs(input_folder, output_folder):
#     for file in os.listdir(input_folder):
#         if file.endswith(".pdf"):
#             input_path = os.path.join(input_folder, file)
#             output_path = os.path.join(output_folder, file.replace(".pdf", ".json"))
#             result = extract_outline_from_pdf(input_path)
#             with open(output_path, "w", encoding="utf-8") as f:
#                 json.dump(result, f, indent=2)

# if __name__ == "__main__":
#     input_dir = "sample_dataset/pdfs"
#     output_dir = "sample_dataset/outputs"
#     os.makedirs(output_dir, exist_ok=True)
#     process_all_pdfs(input_dir, output_dir)



import os
import fitz  # PyMuPDF
import json

# Words to skip from heading extraction
blocked_words = {"overview", "Version"}

def is_heading(text, font_size, font_name):
    if font_size > 15 and "Bold" in font_name:
        return "H1"
    elif font_size > 13:
        return "H2"
    elif font_size > 11:
        return "H3"
    return None

def extract_title_from_first_page(doc):
    first_page = doc[0]
    blocks = first_page.get_text("dict")["blocks"]

    title_candidate = ""
    max_size = 0

    for block in blocks:
        for line in block.get("lines", []):
            text = " ".join(span["text"].strip() for span in line["spans"]).strip()
            if not text or len(text.split()) < 2:
                continue
            span = line["spans"][0]
            size = span["size"]
            font = span["font"]
            is_bold = "Bold" in font or "bold" in font.lower()

            if not is_bold:
                continue

            if any(text.lower().startswith(prefix) for prefix in (
                "table of contents", "revision history", "1.", "2.", "overview"
            )):
                continue

            if size > max_size:
                max_size = size
                title_candidate = text

    return title_candidate or doc.metadata.get("title") or "Untitled"

# def extract_outline_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     outline = []
#     title = extract_title_from_first_page(doc)

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         blocks = page.get_text("dict")["blocks"]
#         for block in blocks:
#             for line in block.get("lines", []):
#                 for span in line.get("spans", []):
#                     text = span["text"].strip()
#                     if len(text) < 3:
#                         continue
#                     if text == title:
#                         continue  # Skip title
#                     if any(b in text.lower() for b in blocked_words):
#                         continue  # Skip if any blocked word appears in heading

#                     heading_level = is_heading(text, span["size"], span["font"])
#                     if heading_level:
#                         outline.append({
#                             "level": heading_level,
#                             "text": text,
#                             "page": page_num + 1
#                         })

#     return {
#         "title": title,
#         "outline": outline
#     }

# def extract_outline_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     outline = []
#     title = extract_title_from_first_page(doc)
#     seen = set()

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         blocks = page.get_text("dict")["blocks"]
#         for block in blocks:
#             for line in block.get("lines", []):
#                 line_text = ""
#                 max_size = 0
#                 font_name = ""
#                 for span in line.get("spans", []):
#                     text = span["text"].strip()
#                     if not text:
#                         continue
#                     line_text += text + " "
#                     if span["size"] > max_size:
#                         max_size = span["size"]
#                         font_name = span["font"]
#                 line_text = line_text.strip()
#                 if (
#                     len(line_text) < 3
#                     or line_text == title
#                     or line_text.lower() in seen
#                     or any(b in line_text.lower() for b in blocked_words)
#                 ):
#                     continue

#                 heading_level = is_heading(line_text, max_size, font_name)
#                 if heading_level:
#                     outline.append({
#                         "level": heading_level,
#                         "text": line_text,
#                         "page": page_num + 1
#                     })
#                     seen.add(line_text.lower())

#     return {
#         "title": title,
#         "outline": outline
#     }


def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    seen = set()
    title = extract_title_from_first_page(doc)
    title = title.strip() if title else ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                max_size = 0
                font_name = ""

                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text:
                        continue
                    line_text += text + " "
                    if span["size"] > max_size:
                        max_size = span["size"]
                        font_name = span["font"]

                line_text = line_text.strip()
                if (
                    len(line_text) < 3 or
                    line_text.lower() in seen or
                    line_text == title or
                    any(b in line_text.lower() for b in blocked_words)
                ):
                    continue

                heading_level = is_heading(line_text, max_size, font_name)
                if heading_level:
                    outline.append({
                        "level": heading_level,
                        "text": line_text,
                        "page": page_num + 1
                    })
                    seen.add(line_text.lower())

    return {
        "title": title or "Untitled",
        "outline": outline
    }



def process_all_pdfs(input_folder, output_folder):
    for file in os.listdir(input_folder):
        if file.endswith(".pdf"):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, file.replace(".pdf", ".json"))
            result = extract_outline_from_pdf(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    input_dir = "sample_dataset/pdfs"
    output_dir = "sample_dataset/outputs"
    os.makedirs(output_dir, exist_ok=True)
    process_all_pdfs(input_dir, output_dir)
