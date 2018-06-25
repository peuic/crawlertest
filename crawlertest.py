"""I started retrieving data from the downloaded lawsuit HTML document using BeautifulSoup.
Identifying the patterns of the tables in the document, i could pull some data such as
lawsuit number, lawyers and parties.

To access differents lawsuits you need to change the number on the file from 1 to 15. Ex: ProcessoX.html

The method for acquiring data may change according to the lawsuit's phase, as shown below.

(Uncomment to see other functions)"""

from bs4 import BeautifulSoup
import re
import urllib3


r = open('/Users/peuic/Documents/Projetos/crawlertest/Processos/Processo1.html', encoding = "ISO-8859-1")
data = r.read()
r.close()
soup = BeautifulSoup(data, 'html.parser')


#GET LAWSUIT REGISTRATION NUMBER:

def get_id():
    s_numproc = soup.find(class_ = 'primeiraLinha')
    numproc = s_numproc.get_text()
    return numproc [14:40]

print(get_id())


#FIND JUDGE AND COURT

def find_judge():
    judge = soup.find('b', string=re.compile(r'Juiz')).parent
    juizz = judge.get_text()
    juiz = juizz.replace ('Histórico de Juízes', '')
    return juiz

print(find_judge())

#GET PARTIES' NAMES (Needs formating):

#Partes Polo Passivo
def get_partiespp():
    partes = soup.find(id = 'tabelaPartes29')
    if partes != None:
        partest = partes.get_text()
        partiespp = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')
        return partiespp
    else:
        partes = soup.find(id = 'tabelaPartes0')
        partest= partes.get_text()
        partiespp = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')
        return partiespp

#Partes Polo Ativo
def get_partiespa():
    partespa = soup.find(id = 'tabelaPartes30')
    if partespa != None:
        partespa_ = partespa.get_text()
        partiespa = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')
        return partiespa
    else:
        partespa = soup.find(id = 'tabelaPartes1')
        partespa_ = partespa.get_text()
        partiespa = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '')   
        return partiespa


print ('\n', 'Polo Passivo: ', get_partiespp()[9:], '\n', 'Polo Ativo: ', get_partiespa()[9:])

#GET LAWYERS DATA:

#ADVOGADOS POLO PASSIVO:

def find_lawpp():
    s_advpp = soup.find(id = 'tabelaAdvogadoPartes29')
    if s_advpp != None:
        advpp = s_advpp.get_text()
        return advpp
    else:
        s_advppc = soup.find(id = 'tabelaAdvogadoPartes0')
        advppc = s_advppc.get_text()
        return advppc


#ADVOGADOS POLO ATIVO:

def find_lawpa():   
    s_advpa = soup.find(id = 'tabelaAdvogadoPartes30')
    if s_advpa != None:
        advpa = s_advpa.get_text()
        return advpa
    else:
        s_advpac = soup.find(id = 'tabelaAdvogadoPartes1')
        advpac_ = s_advpac.get_text()
        return advpac_


print('\n', 'Advogados Polo Ativo:', find_lawpa()[20:], '\n Advogados Polo Passivo:', find_lawpp()[20:])


#GET FOLLOWUP (Needs cleaning):

#def get_followup():
#    table = soup.find('div', id="Arquivos")
#    tablet = table.find('table')
#    andamentos = tablet.find_all_next('td')
#    return andamentos

#print(get_followup())



