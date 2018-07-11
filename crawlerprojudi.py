"""I started retrieving data from the downloaded lawsuit HTML document using BeautifulSoup.
Identifying the patterns of the tables in the document, i could pull some data such as
lawsuit number, lawyers and parties' names."""


from bs4 import BeautifulSoup
import re
import urllib3
from splinter import Browser
import json

proc = '3220182150626'

url = 'https://projudi.tjba.jus.br/projudi/interno.jsp?endereco=/projudi/buscas/ProcessosParte'
url1 = 'https://projudi.tjba.jus.br/projudi/listagens/DadosProcesso?numeroProcesso='+proc

b = Browser('chrome', headless=True)
b.visit(url)
b.visit(url1)
data = b.html
soup = BeautifulSoup(data, 'html.parser')
soupt = BeautifulSoup(data, 'html.parser').text


#GET LAWSUIT REGISTRATION NUMBER:

def get_id():
    soup_numproc = soup.find(class_ = 'primeiraLinha')
    numproc = soup_numproc.get_text()
    law_id = numproc [14:39]
    return law_id

print(get_id())


#FIND JUDGE

def find_judge():
    judges_in = soupt.find('Juiz: ')
    judges_out = soupt.find('Histórico de Juízes')
    judge_ = soupt[judges_in:judges_out] 
    judge = judge_.replace('Juiz: ', '')
    return judge

print(find_judge())

#GET COURT

def get_court():
    juizo_in = soupt.find('Juízo')
    juizo_out = soupt.find('Juiz: ')
    juizo_ = soupt[juizo_in:juizo_out]
    court = juizo_.replace('\n', '').replace('Juízo:', '')
    return court

print(get_court())

#GET LAWSUIT'S CLASS

def get_class():
    classe_in = soupt.find('Classe:')
    classe_out = soupt.find('Segredo de Justiça')
    classe_ = soupt[classe_in:classe_out]
    classe = classe_.replace('\n', '').replace('Este processo possui 1 suspeita de prevenção', '').replace('Este processo possui 2 suspeitas de prevenção',
    '').replace('Classe:', '')
    return classe

print(get_class())

#GET LAWSUIT'S PHASE

def get_phase():
    fase_in = soupt.find('Fase')
    fase_out = soupt.find('Objeto')
    faset = soupt[fase_in:fase_out]
    fase_proc = faset.replace ('\n', '').replace('      ', ' ').replace('Fase  Processual:', '')
    return fase_proc
    
print(get_phase())


#FIND LAWSUIT VALUE

def get_value():
    value_in = soupt.find('Valor da Causa')
    value_out = soupt.find('Último Evento')
    l_value = soupt[value_in:value_out]
    law_value = l_value.replace('\n', '').replace('Valor da Causa: ', '')
    return law_value

print(get_value())

#GET PARTIES' NAMES:

#Partes Polo Passivo
def get_partiespp():
    partes = soup.find(id = 'tabelaPartes29')
    if partes != None:
        partest = partes.get_text()
        partiespp_ = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
        ' ').replace('                            ',' ')
        partiespp = partiespp_[9:]
        return partiespp
    else:
        partes = soup.find(id = 'tabelaPartes0')
        if partes != None:
            partest= partes.get_text()
            partiespp_ = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
            ' ').replace('                            ',' ').replace('                   ', '')
            partiespp = partiespp_[9:] 
            return partiespp
        else:
            partes = soup.find(id = 'tabelaPartes16')
        if partes != None:
            partest= partes.get_text()
            partiespp_ = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
            ' ').replace('                            ',' ')
            partiespp = partiespp_[9:] 
            return partiespp
        else:
             return ''

def get_reu():
    reu_ = soup.find(id = 'tabelaPartes67')
    if reu_ != None:
        reu_t= reu_.get_text()
        reu_tt = reu_t.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
        ' ').replace('                            ', ' ')
        reu = reu_tt[9:] 
        return reu
    else:
        return ''

#Partes Polo Ativo
def get_partiespa():
    partespa = soup.find(id = 'tabelaPartes30')
    if partespa != None:
        partespa_ = partespa.get_text()
        partiespa_ = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
        ' ').replace('                            ', ' ')
        partiespa = partiespa_[9:]
        return partiespa
    else:
        partespa = soup.find(id = 'tabelaPartes1')
        if partespa != None:
            partespa_ = partespa.get_text()
            partiespa_ = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
            ' ').replace('                            ', ' ')   
            partiespa = partiespa_[9:]
            return partiespa
        else:
            partespa = soup.find(id = 'tabelaPartes4')
        if partespa != None:
            partespa_ = partespa.get_text()
            partiespa_ = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
            ' ').replace('                            ', ' ')   
            partiespa = partiespa_[9:]
            return partiespa
        else:
            return ''

def get_autor():
    autor_ = soup.find(id = 'tabelaPartes14')
    if autor_ != None:
        autor_t= autor_.get_text()
        autor_tt = autor_t.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('         ', '').replace('\t',
        ' ').replace('                            ', ' ')
        autor = autor_tt[9:] 
        return autor
    else:
        return ''


print ('Polo Passivo:', get_partiespp(), get_reu(), '\n','Polo Ativo: ', get_partiespa(), get_autor())

#GET LAWYERS DATA:

#ADVOGADOS POLO PASSIVO:

def find_lawpp():
    s_advpp = soup.find(id = 'tabelaAdvogadoPartes29')
    if s_advpp != None:
        advpp_ = s_advpp.get_text()
        advppl = advpp_[20:]
        advpp = advppl.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')
        return advpp
    else:
        s_advppc = soup.find(id = 'tabelaAdvogadoPartes0')
        if s_advppc != None:
            advppc_ = s_advppc.get_text()
            advppce = advppc_[20:]
            advppc = advppce.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')
            return advppc
        else:
            s_advppc = soup.find(id = 'tabelaAdvogadoPartes16')
        if s_advppc != None:
            advppc_ = s_advppc.get_text()
            advppce = advppc_[20:]
            advppc = advppce.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')

            return advppc
        else:
            s_advppc = soup.find(id = 'tabelaAdvogadoPartes67')
        if s_advppc != None:
            advppc_ = s_advppc.get_text()
            advppce = advppc_[20:]
            advppc = advppce.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')

            return advppc
        else:
            return''


#ADVOGADOS POLO ATIVO:

def find_lawpa():   
    s_advpa = soup.find(id = 'tabelaAdvogadoPartes30')
    if s_advpa != None:
        advpa_ = s_advpa.get_text()
        advpae = advpa_[20:]
        advpa = advpae.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')
        return advpa
    else:
        s_advpac = soup.find(id = 'tabelaAdvogadoPartes1')
        if s_advpac != None:
            advpac_ = s_advpac.get_text()
            advpace = advpac_[20:]
            advpac = advpace.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')
            return advpac
        else:
            s_advpac = soup.find(id = 'tabelaAdvogadoPartes4')
        if s_advpac != None:
            advpac_ = s_advpac.get_text()
            advpace = advpac_[20:]
            advpac = advpace.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')
            return advpac
        else:
            s_advpac = soup.find(id = 'tabelaAdvogadoPartes14')
        if s_advpac != None:
            advpac_ = s_advpac.get_text()
            advpace = advpac_[20:]
            advpac = advpace.replace(' ', '-').replace('\n', 
            '_').replace('_----------------------------	_----------------------------	_	---------------------------_',' - ').replace('__','').replace('_',
            '\n').replace('-', ' ').replace('   ', ' ')
            return advpac
        else:
            return ''


print('Advogados Polo Ativo:', find_lawpa(), '\n Advogados Polo Passivo:',find_lawpp())


#GET FOLLOWUP (Needs cleaning):

def get_followup():
    andamentos_in = soupt.find('Arquivos/Observação')
    andamentos_out = soupt.find('var ar = document.getElement')
    follow_ups = soupt[andamentos_in:andamentos_out]
    follow_up = follow_ups.replace('\n\n', '').replace('Movimentação sem arquivos', '').replace('Arquivos/Observação',
     'Andamentos:')
    return follow_up

print(get_followup())

#STORE LAWSUIT DATA

lawsuit = {
    'id': get_id(), 
    'judge': find_judge(), 
    'court': get_court(), 
    'class': get_class(), 
    'phase': get_phase(), 
    'value': get_value(),
    'active party':[ 
        get_partiespa(),
        get_autor()
    ],
    'lawyer active': find_lawpa(),
    'passive party': [
        get_partiespp(),
        get_reu()
    ],
    'lawyer passive': find_lawpp(),
    'follow up': get_followup()
    }



with open(get_id()+'.json', 'w') as outfile:
    json.dump(lawsuit, outfile, ensure_ascii=False, indent=4)






