import google.generativeai as genai
import fitz  # PyMuPDF
import os

from flask import Flask, render_template, request

app = Flask(__name__)

# Chemin vers le répertoire d'uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Définir le répertoire d'uploads dans l'application Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Définir la clé API
os.environ["GOOGLE_API_KEY"] = "AIzaSyBH2VLJnmJYXjGDMapF2X9f1VhaH-pSjVw"

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with fitz.open(pdf_file_path) as pdf_document:
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            text += page.get_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Vérifier si le fichier a été téléchargé
        if 'pdf' not in request.files:
            return render_template('index.html', error='Aucun fichier téléchargé')
        
        pdf_file = request.files['pdf']

        # Vérifier si aucun fichier n'a été sélectionné
        if pdf_file.filename == '':
            return render_template('index.html', error='Aucun fichier sélectionné')

        # Sauvegarder le fichier téléchargé dans le répertoire uploads
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)

        # Extraire le texte du PDF
        pdf_text = extract_text_from_pdf(pdf_path)

        # Appeler l'API d'IA pour obtenir la réponse
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(["j'aimerais recevoir ton feedback sur le compte rendu que j'ai rédigé pour les travaux pratiques portant sur le bras robotique NED2 de Niryo dans le contexte de l'industrie 4.0. Pour cela, je souhaiterais que tu examines les aspects suivants : pertinence des informations fournies sur les fonctionnalités et les performances du bras robotique NED2, clarté et précision de la présentation des résultats des expérimentations et des tests effectués, analyse approfondie des défis rencontrés et des solutions proposées lors de la mise en œuvre des travaux pratiques, pertinence des conclusions tirées et des recommandations formulées pour l'amélioration des performances du système. Je te serais reconnaissant de me fournir tes commentaires structurés de manière claire et concise, en environ 150 mots", pdf_text])
        response1 = model.generate_content(["attribue à ce compte rendu une note sur 20. Donne que la note n'ajoute aucun commentaire je veux en reponse d un numéro sur 20.", pdf_text])

        # Supprimer le fichier PDF soumis après analyse
        os.remove(pdf_path)

        # Renvoyer la réponse vers le template HTML
        return render_template('submit.html', response=response.text , response1=response1.text)
    else:
        return render_template('submit.html')

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/indexx')
def indexx():
    return render_template('indexx.html')

@app.route('/profile')  
def profile():
    return render_template('profile.html')

@app.route('/team')
def team():
    return render_template('TEAM.html')
@app.route('/quizz')
def quizz():
    return render_template('quizz.html')
@app.route('/submitt')
def submitt():
    return render_template('submitt.html')

if __name__ == '__main__':
    app.run(debug=True)
