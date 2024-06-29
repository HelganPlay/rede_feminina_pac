from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os
from queries import check_and_create_table, contar_quantidade_total, pessoas_por_tipo_de_cancer, contar_quantidade_diferentes
from excel_to_mysql import insert_data_from_excel

app = Flask(__name__)

# upload da planilha pra essa pasta
app.config['UPLOAD_FOLDER'] = 'uploads/'
# cria a pasta de uploads se ela não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'rede_feminina'

# caminho do arquivo excel
excel_file_path = os.path.join('uploads', 'planilha.xlsx')

# Inicializar MySQL
mysql = MySQL(app)


@app.route('/')
def index():
    check_and_create_table(mysql)
    valor = contar_quantidade_total(mysql, "Nome")
    tipos_cancer, contagem = contar_quantidade_diferentes(mysql, "tipo_cancer")

    return render_template(r'index.html', valor=valor, tipos_cancer=tipos_cancer, contagens=contagem)


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    filename = 'planilha.xlsx'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return redirect('/excel_to_mysql')


@app.route('/excel_to_mysql')
def inserir_data():

    insert_data_from_excel(mysql, excel_file_path)

    if os.path.exists(excel_file_path):
        # Exclui o arquivo se ele existir
        os.remove(excel_file_path)

    return redirect('/')


@app.route('/receber_arquivo')
def receber_arquivo():

    return render_template('receber_arquivo.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
