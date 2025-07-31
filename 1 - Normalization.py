import spacy
import docx  # for reading .docx files
import os

# Load spaCy English model
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

def read_docx_text(filepath: str) -> str:
    """Read text from a .docx file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

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

# Example usage
if __name__ == "__main__":
    input_file = "Final - R11749001.docx"
    output_file = "Final - R11749001_normalized.txt"
    normalize_docx_and_save(input_file, output_file)
