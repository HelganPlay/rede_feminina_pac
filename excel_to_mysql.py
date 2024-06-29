import pandas as pd
from queries import get_current_year
from unidecode import unidecode

def insert_data_from_excel(mysql, excel_file_path):
    # Ler o arquivo Excel até a coluna 'O'
    df = pd.read_excel(excel_file_path, usecols='A:O')

    # Obter o ano atual e o nome da tabela
    year = get_current_year()
    table_name = f'pacientes_{year}'

    # Conectar ao banco de dados e inserir dados
    cursor = mysql.connection.cursor()

    for _, row in df.iterrows():
        try:
            cursor.execute(f"""
                    INSERT INTO {table_name} (
                        Nome, Data_Nascimento, Idade, Telefone, Endereco, Tipo_Cancer, Data_Cadastro,
                        Servico_Social, Psicologia, Fisioterapia, Acupuntura, Juridico, Reiki,
                        Ginastica, Sempre_Vivas
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                row[0],  # Nome
                row[1],  # data de nasc.
                row[2],  # Idade
                row[3],  # Telefone
                row[4],  # Endereço
                unidecode(row[5]).strip().lower(),  # Tipo_Cancer
                row[6],  # data_cadastro,

                bool(row[7]) if pd.notna(row[7]) else None,  # Servico_Social
                bool(row[8]) if pd.notna(row[8]) else None,  # Psicologia
                bool(row[9]) if pd.notna(row[9]) else None,  # Fisioterapia
                bool(row[10]) if pd.notna(row[10]) else None,  # Acupuntura
                bool(row[11]) if pd.notna(row[11]) else None,  # Juridico
                bool(row[12]) if pd.notna(row[12]) else None,  # Reiki
                bool(row[13]) if pd.notna(row[13]) else None,  # Ginastica
                bool(row[14]) if pd.notna(row[14]) else None  # Sempre_Vivas
            ))
        except Exception as e:
            print(f"Erro ao inserir dados na linha: {row}. Erro: {e}")

    mysql.connection.commit()
    cursor.close()

# Exemplo de uso:
# insert_data_from_excel(mysql_connection_object, '/mnt/data/Planilha estudantes.xlsx')
