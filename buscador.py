from flask import Flask, render_template, request
import re

app = Flask(__name__)

def split_text(text, max_length=3000):
    # Divide o texto em segmentos menores
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Função para buscar informações relevantes no texto extraído do PDF
def search_in_pdf_text(pdf_text, question):
    question = question.lower().strip()
    escaped_question = re.escape(question)

    # Remover números e pontos da pergunta
    question = re.sub(r'[\d\.]+', '', question)

    matches = re.finditer(r'\b(?:%s)\b' % '|'.join(escaped_question.split()), pdf_text.lower())

    response = []
    for match in matches:
        start_index = max(match.start() - 300, 0)
        end_index = min(match.end() + 300, len(pdf_text))
        snippet = pdf_text[start_index:end_index].strip()
        snippet = re.sub(r'\s+', ' ', snippet)
        response.extend(split_text(snippet))

    # Filtra as respostas para remover aquelas que contenham apenas caracteres repetidos ou são muito curtas
    filtered_response = []
    for text in response:
        if len(text) > 50 and not re.match(r'^(\W)\1*$', text):
            filtered_response.append(text)

    if filtered_response:
        return filtered_response[:20]
    else:
        return ["Nenhuma informação relevante encontrada."]

# Caminho para o arquivo de texto extraído do PDF
pdf_text_file = "texto_extraido.txt"

with open(pdf_text_file, "r", encoding="utf-8") as file:
    pdf_text = file.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    response = search_in_pdf_text(pdf_text, question)
    return render_template('index.html', question=question, response=response)

if __name__ == '__main__':
    app.run(debug=True)
