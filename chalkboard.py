"""I started retrieving data from the downloaded lawsuit HTML document using BeautifulSoup.
Identifying the patterns of the tables in the document, i could pull some data such as
lawsuit number, lawyers and parties' names.

To access differents lawsuits you need to change the number on the file from 1 to 19. Ex: ProcessoX.html"""


from bs4 import BeautifulSoup
import re
import urllib3


r = open('/Users/peuic/Documents/Projetos/crawlertest/Processos/Processo1.html', encoding = "ISO-8859-1")
data = r.read()
r.close()
soup = BeautifulSoup(data, 'html.parser')
soupt = BeautifulSoup(data, 'html.parser').text




def clean_text():
        tabs_removed = soupt.replace("\t", "")
        lines = tabs_removed.split("\n")
        return "\n".join([line for line in lines if line.strip() != ""])

def clean_tags(self, html=None):
        tags_to_clean = ["script", "style", "select", "option"]
        for tag in tags_to_clean:
            [t.decompose() for t in html.find_all(tag)]
        return html

#GET LAWSUIT REGISTRATION NUMBER:

def get_id():
    s_numproc = soup.find(class_ = 'primeiraLinha')
    numproc = s_numproc.get_text()
    proc_id = numproc [14:39]
    return proc_id

#print(get_id())


#FIND JUDGE

def find_judge():
    judges_in = soupt.find('Juiz: ')
    judges_lim = soupt.find('Histórico de Juízes')
    judge = soupt[judges_in:judges_lim] 
    return judge

#print(find_judge())

#GET COURT

def get_court():
    juizo_in = soupt.find('Juízo')
    juizo_lim = soupt.find('Juiz: ')
    juizo_ = soupt[juizo_in:juizo_lim]
    juizo = juizo_.replace('\n', '')
    return juizo

#print(get_court())

#GET LAWSUIT'S CLASS

def get_class():
    classe_in = soupt.find('Classe:')
    classe_out = soupt.find('Segredo de Justiça')
    classe_ = soupt[classe_in:classe_out]
    classe = classe_.replace('\n', '').replace('Este processo possui 1 suspeita de prevenção', '')
    return classe

#print(get_class())

#GET LAWSUIT'S PHASE

def get_phase():
    fase = soupt.find('Fase')
    fase_lim = soupt.find('Objeto')
    faset = soupt[fase:fase_lim]
    fase_proc = faset.replace ('\n', '').replace('      ', ' ')
    return fase_proc
    
#print(get_phase())


#FIND LAWSUIT VALUE

def get_value():
    val = soupt.find('Valor da Causa')
    val_l = soupt.find('Último Evento')
    l_value = soupt[val:val_l]
    law_value = l_value.replace('\n', '')
    return law_value

#print(get_value())

#GET PARTIES' NAMES:

#Partes Polo Passivo
def get_partiespp():
    partes = soup.find(id = 'tabelaPartes29')
    if partes != None:
        partest = partes.get_text()
        partiespp = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
        return partiespp
    else:
        partes = soup.find(id = 'tabelaPartes0')
        if partes != None:
            partest= partes.get_text()
            partiespp_ = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
            partiespp = partiespp_[9:] 
            return partiespp
        else:
            partes = soup.find(id = 'tabelaPartes16')
        if partes != None:
            partest= partes.get_text()
            partiespp_ = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
            partiespp = partiespp_[9:] 
            return partiespp
        else:
            return ''

#Partes Polo Ativo
def get_partiespa():
    partespa = soup.find(id = 'tabelaPartes30')
    if partespa != None:
        partespa_ = partespa.get_text()
        partiespa = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
        return partiespa
    else:
        partespa = soup.find(id = 'tabelaPartes1')
        if partespa != None:
            partespa_ = partespa.get_text()
            partiespa_ = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')  
            partiespa = partiespa_[9:]
            return partiespa
        else:
            partespa = soup.find(id = 'tabelaPartes4')
        if partespa != None:
            partespa_ = partespa.get_text()
            partiespa_ = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
        '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
            partiespa = partiespa_[9:]
            return partiespa
        else:
            return ''


#print ('Polo Passivo:', get_partiespp(), '\n','Polo Ativo: ', get_partiespa(), '\n')

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
            s_advppc = soup.find(id = 'tabelaAdvogadoPartes16')
        if s_advppc != None:
            advppc_ = s_advppc.get_text()
            advppc = advppc_[20:]
            return advppc
        else:
            s_advppc = soup.find(id = 'tabelaAdvogadoPartes67')
        if s_advppc != None:
            advppc_ = s_advppc.get_text()
            advppc = advppc_[20:]
            return advppc
        else:
            return''


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
            s_advpac = soup.find(id = 'tabelaAdvogadoPartes4')
        if s_advpac != None:
            advpac_ = s_advpac.get_text()
            advpac = advpac_[20:]
            return advpac
        else:
            return ''

#print('Advogados Polo Ativo:', find_lawpa(), '\n Advogados Polo Passivo:',find_lawpp())

#GET FOLLOWUP (Needs cleaning):

def get_followup():
    andamentos_ini = soupt.find('Arquivos/Observação')
    andamentos_fim = soupt.find('var ar = document.getElement')
    follow_ups = soupt[andamentos_ini:andamentos_fim]
    follow_up = follow_ups.replace('\n\n', '')
    return follow_up

#print(get_followup())

#GET SUBJECT

def get_subject():
    subject_in = soupt.find('Assunto:')
    subject_out = soupt.find('Complementares:')
    subject_full = soupt[subject_in:subject_out]
    subject = subject_full.replace('\n','').replace('Assunto:','').replace('\xa0\xa0', '')
    return subject

#DATA DE DISTRIBUIÇAO

def get_date():    
    data_in = soupt.find('Data de Distribuição')
    data_out = soupt.find(' às ')
    data_ = soupt[data_in:data_out]
    date = data_.replace('Data de Distribuição\n ', '')
    return date    

#GET LAWSUIT SITUATION

def get_situation():
    situation_in = soupt.find('Situação:')
    situation_out = soupt.find('Data de Distribuição')
    situation_full = soupt[situation_in:situation_out]
    situation = situation_full.replace('\n', '')
    return situation


def get_last_event():
    last_event_in = soupt.find('Último Evento')
    last_event_out = soupt.find('Cartório Extrajudicial:')
    last_event_full = soupt[last_event_in:last_event_out]
    last_event = last_event_full.replace('\n', '').replace('Último Evento', '')
    return last_event


def extract_lawsuit_value():
    text = soup.get_text()
    declared_value = re.search(r"\n?R\$(.*)\n", text)
    return declared_value

#print(extract_lawsuit_value())

def lawsuit_value(soup):
    text = soup.get_text()
    declared_value = re.search(r"\n?R\$(.*)\n", text)
    values = {"declared_value": ""}
    if declared_value:
        values["declared_value"] = declared_value.groups()[0].strip()
    return values

#print(lawsuit_value(soup))


def folup():
    andamentos = {}
    i = 0
    for td in soup.find_all(size='2'):
        followup = td.next_element
        details_ = followup.next_element.next_element.next_element
        details = str(details_)
        date_ = details_.next_element.next_element
        datet = str(date_)
        date = datet.replace('<td align="center" nowrap="" width="100">', '').replace('</td>','')
        print(followup)
        if date != '\n':
            andamentos.update({'andamento'+str(i):[date,followup, details]})
            i += 1
    return andamentos

#print(folup())


additional_info = {
    'id': get_id(),
    'judge': find_judge(),
    'court': get_court(),
    'latest event': get_last_event(),
    'subject': get_subject(),
    'situation': get_situation()
}

#REGEX ATTEMPT

#Lawsuit ID
def extract_lawsuit_id():
        matcher = re.compile(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}.\d{4}")
        result = matcher.search(soupt)
        if result:
            return result.group()
        return None

print(extract_lawsuit_id())

#JUDGE (ToFix)
def extract_lawsuit_judge():
    extract_judge_regex = re.compile(r"Juiz:([\w ]+)\b ?His")
    results = extract_judge_regex.search(soupt)
    if results:
        return results.group()
    return None

print(extract_lawsuit_judge())

#LAWSUIT VALUE

def lawsuit_value():
    declared_value = re.search(r"\n?R\$(.*)", soupt)
    if declared_value:
        return declared_value.group()
    return None

print(lawsuit_value())

#PARTIES (Broken)
def extract_lawsuit_parties():
    extract_party_regex = re.compile(r"Executado([\w ]+)")
    results = extract_party_regex.search(soupt)
    if results:
        return results.group()
    return None

print(extract_lawsuit_parties())

#CLASS
def extract_lawsuit_class():
    extract_class_regex = re.compile(r"Prioridade Processual:(.*)")
    results = extract_class_regex.search(soupt)
    if results:
        return results.group()
    return None

print(extract_lawsuit_class())