import sqlite3
import readchar 
from datetime import date, datetime
from prettytable import PrettyTable


def condicoes_data():
    while True: 
        print("Data (dd/mm/yyyy): ", end = '', flush=True)
        data_entrada = "" 
        while len(data_entrada) < 10: 
            tecla = readchar.readchar(); 
            if tecla in('\x08', '\x7f'):
                if len(data_entrada) > 0:
                    if data_entrada.endswith('/'):
                        data_entrada= data_entrada[:-2]
                        print('\b\b \b\b', end = ' ', flush = True)
                    else: 
                        data_entrada = data_entrada[:-1]
                        print('\b \b', end = '', flush = True)
                    continue 
            if not tecla.isdigit(): 
                continue 
            data_entrada+=tecla 
            print(tecla, end = '', flush=True)
                
            if len(data_entrada) == 2 or len(data_entrada)==5:
                data_entrada+='/'
                print('/', end = '', flush = True)
        print() 
        try:
            datetime.strptime(data_entrada, "%d/%m/%Y")
            return data_entrada 
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
