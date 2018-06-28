"""I started retrieving data from the downloaded lawsuit HTML document using BeautifulSoup.
Identifying the patterns of the tables in the document, i could pull some data such as
lawsuit number, lawyers and parties' names.

To access differents lawsuits you need to change the number on the file from 1 to 17. Ex: ProcessoX.html"""


from bs4 import BeautifulSoup
import re
import urllib3


r = open('/Users/peuic/Documents/Projetos/crawlertest/Processos/Processo17.html', encoding = "ISO-8859-1")
data = r.read()
r.close()
soup = BeautifulSoup(data, 'html.parser')
soupt = BeautifulSoup(data, 'lxml').text


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


#FIND LAWSUIT VALUE

def get_value():
    val = soupt.find('Valor da Causa')
    val_l = soupt.find('Último Evento')
    l_value = soupt[val:val_l]
    return l_value

print(get_value())

#GET PARTIES' NAMES (Needs formating):

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


print ('\n', 'Polo Passivo: ', get_partiespp(), '\n', 'Polo Ativo: ', get_partiespa(), '\n')

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


print('Advogados Polo Ativo:', find_lawpa(), '\n Advogados Polo Passivo:', find_lawpp())


#GET FOLLOWUP (Needs cleaning):

def get_followup():
    andamentos_ini = soupt.find('Arquivos/Observação')
    andamentos_fim = soupt.find('var ar = document.getElement')
    follow_ups = soupt[andamentos_ini:andamentos_fim]
    follow_up = follow_ups.replace('\n\n', '')
    return follow_up

#print(get_followup())


