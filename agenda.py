import sqlite3
from datetime import date
from prettytable import PrettyTable


def condicoes_data():
    is_valid = True
    while is_valid:
        cont = 0
        data_evento = input("Data(dd/mm/yyyy): ")
        for item in data_evento:
            if item == "/":
                cont +=1
        if cont ==2:
            list_data_evento = data_evento.split("/")
            
            if int(list_data_evento[0]) > 0 and int(list_data_evento[0])<32\
                and int(list_data_evento[1])>0 and int(list_data_evento[1])<13\
                and int(list_data_evento[2])>0:
                
                if len(list_data_evento[0]) == 2\
                    and len(list_data_evento[1])== 2\
                    and len(list_data_evento[2]) == 4:
                    
                    return data_evento
                else:
                    is_valid = True
            else:
                is_valid = True
        else:
            is_valid = True
         
tabela = PrettyTable()
tabela.field_names = ["Evento", "Data", "Tempo restante"]

data_atual = date.today()
data_formatada = data_atual.strftime('%d/%m/%Y')
data_formatada_list = data_formatada.split("/")

conexao = sqlite3.connect("agenda.db")
cursor = conexao.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Agenda(
            id INTEGER PRIMARY KEY, 
            data TEXT, 
            evento CHAR(64)
            
        )''')

conexao.commit() 
leitura_edicao = input("Ver/adicionar data [Q/E]: ").lower()

if leitura_edicao == "e":
    evento = input("Evento: ")
    data_evento = condicoes_data()
    
    cursor.execute('''
        INSERT INTO Agenda(data, evento) values(?, ?);    
                             
        ''', (data_evento, evento))
    conexao.commit()

if leitura_edicao == "q":
    cursor.execute('''
            SELECT * FROM Agenda  
                    
            ''')

    for itens in cursor.fetchall():
        data_list = itens[1].split("/")
    
        dia_atual = int(data_formatada_list[0])
        dia_evento = int(data_list[0])
        
        mes_atual = int(data_formatada_list[1])*30
        mes_evento = int(data_list[1])*30
        
        ano_atual = int(data_formatada_list[2])*365
        ano_evento = int(data_list[2])*365
        
        tempo_atual = mes_atual+ano_atual+dia_atual
        tempo_evento = dia_evento+mes_evento+ano_evento
        
        evento = itens[2]
        data_evento = itens[1]
        tempo_rest = tempo_evento-tempo_atual
        
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
        
        tabela.add_row([evento, data_evento, tempo_resto_format])
        tabela.add_row(["", "",  ""])
    print(tabela)
