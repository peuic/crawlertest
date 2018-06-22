"""I started retrieving data from the downloaded lawsuit HTML document using BeautifulSoup.
Identifying the patterns of the tables in the document, i could pull some data such as
lawsuit number, lawyers and parties. However, the parties names still
comes with some useless data, like undeclared infos.

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

#GET PARTIES' NAMES:

#def get_parties():
    #partes = soup.find(class_ = 'tabelaLista')
    #partest = partes.get_text()
    #return(partest)

#print (get_parties())

#GET LAWYERS DATA (lawsuits in execution phase):

#ADVOGADOS POLO PASSIVO:

#def find_lawpp():
    #s_advpp = soup.find(id = 'tabelaAdvogadoPartes29')
    #advpp = s_advpp.get_text()
    #return advpp

#ADVOGADOS POLO ATIVO:

#def find_lawpa():   
    #s_advpa = soup.find(id = 'tabelaAdvogadoPartes30')
    #advpa = s_advpa.get_text()
    #return advpa

#print('Advogado(s) - Polo Ativo: \n\n', find_lawpa()[20:], 'Advogado(s) - Polo Passivo:\n\n', find_lawpp()[20:])

#GET LAWYERS DATA (lawsuits in 'knowledge' phase):

#ADVOGADOS POLO PASSIVO:

#def find_lawpp():    
    #s_advpp = soup.find(id = 'tabelaAdvogadoPartes0')
    #advpp = s_advpp.get_text()
    #return advpp

#ADVOGADOS POLO ATIVO:

#def find_lawpa():
    #s_advpa = soup.find(id = 'tabelaAdvogadoPartes1')
    #advpa = s_advpa.get_text()
    #return advpa

#print('Advogado(s) - Polo Ativo: \n\n', find_lawpa()[20:], 'Advogado(s) - Polo Passivo:\n\n', find_lawpp()[20:])   

#GET FOLLOWUP (Needs cleaning):

def get_followup():
    table = soup.find('div', id="Arquivos")
    tablet = table.find('table')
    andamentos = tablet.find_all_next('font', size="2")
    return andamentos

print(get_followup())
   


