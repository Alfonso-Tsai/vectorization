import spacy
import docx  # for reading .docx files
import os
import re

# Load spaCy English model
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# Specify the folder path
folder_path = "Testing Data"
output_folder = "Normalized Data"

  # Define keyword library (lowercase for comparison)
HEADER_KEYWORDS = {
        "chatgpt",
        "chat gpt",
        "feedback",
        "comment",
        "advice",
        "suggestion",
        "improvement",
        "improved",
        "revision",
        "review",
        "peer",
        "ai",
        "final"
    }

STUDENT_ID_PATTERN = re.compile(r"\b[ABRT]\d{8}\b", re.IGNORECASE)

# Ensure the output folder exists and clean it
os.makedirs(output_folder, exist_ok=True)
for f in os.listdir(output_folder):
    file_path = os.path.join(output_folder, f)
    if os.path.isfile(file_path):
        os.remove(file_path)


def read_docx_text(filepath: str) -> str:
    """Read text from a .docx file and remove top lines containing predefined keywords."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Extract non-empty paragraph text
    doc = docx.Document(filepath)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

    # Step 1: Remove header lines (first two lines with keywords)
    for i in range(min(2, len(paragraphs))):
        line = paragraphs[i].lower()
        if any(keyword in line for keyword in HEADER_KEYWORDS):
            paragraphs[i] = ""

    # Step 2: Remove any line containing a student ID
    cleaned_paragraphs = [
        p for p in paragraphs
        if p and not STUDENT_ID_PATTERN.search(p)
    ]

    return "\n".join(cleaned_paragraphs)


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, remove stopwords/punctuation, lemmatize."""
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(tokens)

def normalize_docx_and_save(input_path: str, output_path: str):
    """Process a .docx file and save the normalized text to a .txt file."""
    raw_text = read_docx_text(input_path)
    normalized_text = normalize_text(raw_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(normalized_text)
    print(f"✅ Normalized text saved to: {output_path}")

if __name__ == "__main__":
    # Get a list of all .docx files in the folder
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".docx") and os.path.isfile(os.path.join(folder_path, f))
    ]

    for file in files:
        filename = os.path.splitext(os.path.basename(file))[0]
        output_file = os.path.join(output_folder, f"{filename}_normalized.txt")
        normalize_docx_and_save(file, output_file)

    