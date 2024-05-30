import PyPDF2
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in tqdm(range(num_pages), desc="Extracting Text", unit="page"):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Caminho para o arquivo PDF
pdf_path = "Dispositivos Eletronicos.pdf"

# Extrair texto do PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Armazenar o texto extraído para consulta posterior
with open("texto_extraido.txt", "w", encoding="utf-8") as output_file:
    output_file.write(pdf_text)

print("Texto do PDF extraído e armazenado com sucesso!")
