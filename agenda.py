import sqlite3
from datetime import date, datetime
from prettytable import PrettyTable


def condicoes_data():
    while True: 
        data_evento = input("Data (dd/mm/yyyy): ") 
        try: 
            datetime.strptime(data_evento, "%d/%m/%Y")
            return data_evento
        except ValueError:
            print("Data inválida")  
         
tabela = PrettyTable()
tabela.field_names = ["Evento", "Data", "Tempo restante"]

data_atual = date.today()

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Agenda(
            id INTEGER PRIMARY KEY, 
            data TEXT, 
            evento CHAR(512)
            
        )''')

conexao.commit() 
leitura_edicao = input("Ver/adicionar data [Q/E]: ").strip().lower()

if leitura_edicao == "e":
    evento = input("Evento: ")
    data_evento = condicoes_data()
    
    cursor.execute('''
        INSERT INTO Agenda(data, evento) values(?, ?);                         
        ''', (data_evento, evento))
    conexao.commit()

elif leitura_edicao == "q":
    cursor.execute('''SELECT * FROM Agenda ''')

    for itens in cursor.fetchall():
        evento = itens[2]
        data_evento_str = itens[1] 
        
        data_evento_obj = datetime.strptime(data_evento_str, "%d/%m/%Y").date() 
        tempo_rest = (data_evento_obj-data_atual).days 
        
        if tempo_rest <= 20 and tempo_rest > 0:
            cor =  '\033[1;31;40m'
        else:
            cor = '\033[1;32;40m'
    
        if tempo_rest < 0:
            tempo_resto_format = '\033[1;34;40m'+"FINALIZADO"+"\033[m"
        elif tempo_rest == 0:
            tempo_resto_format = "HOJE"
        else:
            tempo_resto_format = (f"{cor}"+f"{tempo_rest} dia{'s' if tempo_rest > 1 else''}"+"\033[m") 
        
        tabela.add_row([evento, data_evento_str, tempo_resto_format])
        tabela.add_row(["", "",  ""])
    print(tabela)
