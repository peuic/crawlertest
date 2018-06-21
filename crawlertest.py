"""I started retrieving data from the downloaded lawsuit HTML document using BeautifulSoup.
Identifying the patterns of the tables in the document, i could pull datas such as
lawsuit number, lawyers and parties. However, the parties names still
comes with some useless data, like undeclared infos.

To access differents lawsuits you need to change the number on the file from 1 to 15. Ex: ProcessoX.html

The method for acquiring data may change according to the lawsuit's phase, as shown below.

(Uncomment to see other functions)"""

from bs4 import BeautifulSoup
import re
#import urllib3


r = open('/Users/peuic/Documents/Projetos/crawlertest/Processos/Processo1.html', encoding = "ISO-8859-1")
data = r.read()
r.close()
soup = BeautifulSoup(data, 'html.parser')

#GET LAWSUIT REGISTRATION NUMBER:

s_numproc = soup.find(class_ = 'primeiraLinha')
numproc = s_numproc.get_text()
print('\n', numproc [14:40])

#GET PARTIES' NAMES:

#partes = soup.find(class_ = 'tabelaLista')
#partest = partes.get_text()
#print(partest)

#GET LAWYERS DATA (lawsuits in execution phase):

#ADVOGADOS POLO PASSIVO:

s_advpp = soup.find(id = 'tabelaAdvogadoPartes29')
advpp = s_advpp.get_text()

#ADVOGADOS POLO ATIVO:

s_advpa = soup.find(id = 'tabelaAdvogadoPartes30')
advpa = s_advpa.get_text()

print('Advogado(s) - Polo Ativo: \n\n', advpa[20:], 'Advogado(s) - Polo Passivo:\n\n', advpp[20:])

#GET LAWYERS DATA (lawsuits in 'knowledge' phase):

#ADVOGADOS POLO PASSIVO:

#s_advpp = soup.find(id = 'tabelaAdvogadoPartes0')
#advpp = s_advpp.get_text()

#ADVOGADOS POLO ATIVO:

#s_advpa = soup.find(id = 'tabelaAdvogadoPartes1')
#advpa = s_advpa.get_text()

#print('Advogado(s) - Polo Ativo: \n\n', advpa[20:], 'Advogado(s) - Polo Passivo:\n\n', advpp[20:])   
