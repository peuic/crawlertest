"""I started retrieving data from the downloaded lawsuit HTML document using BeautifulSoup.
Identifying the patterns of the tables in the document, i could pull some data such as
lawsuit number, lawyers and parties' names.

To access differents lawsuits you need to change the number on the file from 1 to 19. Ex: ProcessoX.html"""


from bs4 import BeautifulSoup
import re
import urllib3
from splinter import Browser

url = 'https://projudi.tjba.jus.br/projudi/interno.jsp?endereco=/projudi/buscas/ProcessosParte'
url1 = 'https://projudi.tjba.jus.br/projudi/listagens/DadosProcesso?numeroProcesso=3220152991538'

b = Browser('chrome', headless=True)
b.visit(url)
b.visit(url1)
data = b.html
soup = BeautifulSoup(data, 'html.parser')
soupt = BeautifulSoup(data, 'html.parser').text


#GET LAWSUIT REGISTRATION NUMBER:

def get_id():
    s_numproc = soup.find(class_ = 'primeiraLinha')
    numproc = s_numproc.get_text()
    proc_id = numproc [14:40]
    return proc_id

print(get_id())


#FIND JUDGE

def find_judge():
    judges_in = soupt.find('Juiz: ')
    judges_lim = soupt.find('Histórico de Juízes')
    judge = soupt[judges_in:judges_lim] 
    return judge

print(find_judge())

#GET COURT

def get_court():
    juizo_in = soupt.find('Juízo')
    juizo_lim = soupt.find('Juiz: ')
    juizo_ = soupt[juizo_in:juizo_lim]
    juizo = juizo_.replace('\n', '')
    return juizo

print(get_court())

#GET LAWSUIT'S PHASE

def get_phase():
    fase = soupt.find('Fase')
    fase_lim = soupt.find('Objeto')
    faset = soupt[fase:fase_lim]
    fase_proc = faset.replace ('\n', '').replace('      ', ' ')
    return fase_proc
    
print(get_phase())


#FIND LAWSUIT VALUE

def get_value():
    val = soupt.find('Valor da Causa')
    val_l = soupt.find('Último Evento')
    l_value = soupt[val:val_l]
    law_value = l_value.replace('\n', '')
    return law_value

print(get_value())

#GET PARTIES' NAMES:

#Partes Polo Passivo
def get_partiespp():
    partes = soup.find(id = 'tabelaPartes29')
    if partes != None:
        partest = partes.get_text()
        partiespp_ = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')
        partiespp = partiespp_[9:]
        return partiespp
    else:
        partes = soup.find(id = 'tabelaPartes0')
        if partes != None:
            partest= partes.get_text()
            partiespp_ = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')
            partiespp = partiespp_[9:] 
            return partiespp
        else:
            return ''

#Partes Polo Ativo
def get_partiespa():
    partespa = soup.find(id = 'tabelaPartes30')
    if partespa != None:
        partespa_ = partespa.get_text()
        partiespa_ = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')
        partiespa = partiespa_[9:]
        return partiespa
    else:
        partespa = soup.find(id = 'tabelaPartes1')
        if partespa != None:
            partespa_ = partespa.get_text()
            partiespa_ = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')   
            partiespa = partiespa_[9:]
            return partiespa
        else:
            return ''


print ('Polo Passivo:', get_partiespp(), '\n','Polo Ativo: ', get_partiespa(), '\n')

#GET LAWYERS DATA:

#ADVOGADOS POLO PASSIVO:

def find_lawpp():
    s_advpp = soup.find(id = 'tabelaAdvogadoPartes29')
    if s_advpp != None:
        advpp_ = s_advpp.get_text()
        advpp = advpp_[20:]
        return advpp
    else:
        s_advppc = soup.find(id = 'tabelaAdvogadoPartes0')
        if s_advppc != None:
            advppc_ = s_advppc.get_text()
            advppc = advppc_[20:]
            return advppc
        else:
            return ''


#ADVOGADOS POLO ATIVO:

def find_lawpa():   
    s_advpa = soup.find(id = 'tabelaAdvogadoPartes30')
    if s_advpa != None:
        advpa_ = s_advpa.get_text()
        advpa = advpa_[20:]
        return advpa
    else:
        s_advpac = soup.find(id = 'tabelaAdvogadoPartes1')
        if s_advpac != None:
            advpac_ = s_advpac.get_text()
            advpac = advpac_[20:]
            return advpac
        else:
            return ''


print('Advogados Polo Ativo:', find_lawpa(), '\n Advogados Polo Passivo:',find_lawpp())


#GET FOLLOWUP (Needs cleaning):

def get_followup():
    andamentos_ini = soupt.find('Arquivos/Observação')
    andamentos_fim = soupt.find('var ar = document.getElement')
    follow_ups = soupt[andamentos_ini:andamentos_fim]
    follow_up = follow_ups.replace('\n\n', '').replace('Movimentação sem arquivos', '').replace('Arquivos/Observação', 'Andamentos:')
    return follow_up

print(get_followup())



