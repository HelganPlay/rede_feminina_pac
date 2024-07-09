import datetime

def pegar_ano_atual():
    return datetime.datetime.now().year

year = pegar_ano_atual()

# CREATE
def criar_tabela_para_o_ano(mysql):
    table_name = f'pacientes_{year}'
    cursor = mysql.connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            Nome VARCHAR(255),
            Data_Nascimento DATE,
            Idade INT,
            Telefone VARCHAR(255),
            Endereco VARCHAR(255),
            Tipo_Cancer VARCHAR(255),
            Data_Cadastro DATE,
            Servico_Social BOOL,
            Psicologia BOOL,
            Fisioterapia BOOL,
            Acupuntura BOOL,
            Juridico BOOL,
            Reiki BOOL,
            Ginastica BOOL,
            Sempre_Vivas BOOL
        )
    """)
    mysql.connection.commit()
    cursor.close()


# READ
def contar_quantidade_total(mysql, coluna):
    cursor = mysql.connection.cursor()
    cursor.execute(f""" 
    SELECT COUNT({coluna}) AS Quantidade_total
    FROM pacientes_{year};""")
    valor = cursor.fetchone()[0]
    cursor.close()
    return valor

# READ
def contar_quantidade_diferentes(mysql, coluna, limite):
    cursor = mysql.connection.cursor()
    cursor.execute(f"""SELECT {coluna}, COUNT(*) as count
                        FROM pacientes_{year}
                        GROUP BY {coluna}
                        LIMIT {limite}
                        ;""")
    valor = cursor.fetchall()
    tipos_cancer = [row[0] for row in valor]
    contagens = [row[1] for row in valor]

    cursor.close()
    return tipos_cancer, contagens


