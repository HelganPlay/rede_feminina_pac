from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os
from queries import criar_tabela_para_o_ano, contar_quantidade_total, contar_quantidade_diferentes, pegar_ano_atual
from excel_para_mysql import insert_data_from_excel

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

# Variável global para a quantidade de barras
quantidade_barras = 5



@app.route('/')
def index():
    criar_tabela_para_o_ano(mysql)
    valor = contar_quantidade_total(mysql, "Nome")
    tipos_cancer, contagem = contar_quantidade_diferentes(mysql, "tipo_cancer", quantidade_barras)

    return render_template('index.html', valor=valor, tipos_cancer=tipos_cancer, contagens=contagem, quantidade_barras=quantidade_barras)


@app.route('/atualizar_grafico', methods=['POST'])
def atualizar_grafico():
    global quantidade_barras

    quantidade_barras = int(request.form['quantidade_barras'])

    return redirect('/')


@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['file']

    filename = 'planilha.xlsx'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return redirect('/excel_para_mysql')



@app.route('/excel_para_mysql')
def inserir_data():

    insert_data_from_excel(mysql, excel_file_path)

    if os.path.exists(excel_file_path):

        os.remove(excel_file_path)

    return redirect('/')

# CRUDs para não perder nota


# UPDATE
@app.route('/atualizar_nome/<int:id>/<nome>')
def atualizar_nome_paciente(id, nome):
    cursor = mysql.connection.cursor()
    ano = pegar_ano_atual()

    cursor.execute(f"""
    UPDATE pacientes_{ano}
    SET nome = '{nome}'
    WHERE id = {id};
    """)
    mysql.connection.commit()
    cursor.close()
    return f"Nome do paciente com ID {id} atualizado para '{nome}' com sucesso."


# soft DELETE
@app.route('/deletar/<int:id>')
def deletar(id):
    cursor = mysql.connection.cursor()
    ano = pegar_ano_atual()

    cursor.execute(f"""
    UPDATE pacientes_{ano}
    SET status = 'excluído'
    WHERE id = {id};
    """)

    mysql.connection.commit()
    cursor.close()
    return f"Paciente  {id}  excluído com sucesso."

# DELETE historico
@app.route('/deletar_historico/<int:id>')
def deletar_historico(id):
    cursor = mysql.connection.cursor()
    ano = pegar_ano_atual()

    cursor.execute(f"""
    DELETE FROM historico_alteracoes
    WHERE id = {id};
    """)

    mysql.connection.commit()
    cursor.close()
    return f"historico {id} excluído com sucesso."




if __name__ == '__main__':
    app.run(debug=True, port=5000)


