from bs4 import BeautifulSoup
import re
import urllib3
from splinter import Browser
import json
from urllib.parse import urlencode, urlparse

r = open('/Users/peuic/Documents/Projetos/crawlertest/ProcessosParte5.html', encoding='ISO-8859-1')
data = r.read()
r.close()
sup = BeautifulSoup (data, 'html.parser')

linklist = sup.find_all('a', class_='style2')

ids_links = []
law_ids = []

for link in linklist:
    ids_links.append(link.get('href'))

for link in ids_links:
    law_ids.append(link[48:])

#def _get_capabilities():
#        proxy = {'http':'//35.198.15.121:3128/'}
#        url = urlparse(proxy.get("http", ""))
#        hostname_and_port = "{}:{}".format(url.hostname, url.port)
#        return {
#            "proxy": {
#                "proxyType": "manual",
#                "httpProxy": hostname_and_port,
#                "sslProxy": hostname_and_port,
#            }
#        }
    

#capabilities = _get_capabilities()

for idd in law_ids:
    url0 = 'https://projudi.tjba.jus.br/projudi/interno.jsp?endereco=/projudi/buscas/ProcessosParte'
    url1 = 'https://projudi.tjba.jus.br/projudi/listagens/DadosProcesso?numeroProcesso='+idd

    b = Browser('chrome', headless=True)
    b.visit(url0)
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

    #FIND JUDGE

    def find_judge():
        judges_in = soupt.find('Juiz: ')
        judges_out = soupt.find('Histórico de Juízes')
        judge_ = soupt[judges_in:judges_out] 
        judge = judge_.replace('Juiz: ', '')
        return judge
  
    #GET COURT

    def get_court():
        juizo_in = soupt.find('Juízo')
        juizo_out = soupt.find('Juiz: ')
        juizo_ = soupt[juizo_in:juizo_out]
        court = juizo_.replace('\n', '').replace('Juízo:', '')
        return court

    #DATA DE DISTRIBUIÇAO

    def get_date():    
        data_in = soupt.find('Data de Distribuição')
        data_out = soupt.find(' às ')
        data_ = soupt[data_in:data_out]
        date = data_.replace('Data de Distribuição\n ', '')
        return date

    #GET LAWSUIT'S CLASS

    def get_class():
        classe_in = soupt.find('Classe:')
        classe_out = soupt.find('Segredo de Justiça')
        classe_ = soupt[classe_in:classe_out]
        classe = classe_.replace('\n', '').replace('Este processo possui 1 suspeita de prevenção', '').replace('Este processo possui 2 suspeitas de prevenção',
        '').replace('Classe:', '')
        return classe

    #GET SUBJECT

    def get_subject():
        subject_in = soupt.find('Assunto:')
        subject_out = soupt.find('Complementares:')
        subject_full = soupt[subject_in:subject_out]
        subject = subject_full.replace('\n','').replace('Assunto:','')
        return subject

    #GET LAWSUIT'S PHASE

    def get_phase():
        fase_in = soupt.find('Fase')
        fase_out = soupt.find('Objeto')
        faset = soupt[fase_in:fase_out]
        fase_proc = faset.replace ('\n', '').replace('      ', ' ').replace('Fase  Processual:', '')
        return fase_proc
        
    #FIND LAWSUIT VALUE

    def get_value():
        value_in = soupt.find('Valor da Causa')
        value_out = soupt.find('Último Evento')
        l_value = soupt[value_in:value_out]
        law_value = l_value.replace('\n', '').replace('Valor da Causa: ', '')
        return law_value

    #GET LAWSUIT SITUATION

    def get_situation():
        situation_in = soupt.find('Situação:')
        situation_out = soupt.find('Data de Distribuição')
        situation_full = soupt[situation_in:situation_out]
        situation = situation_full.replace('\n', '').replace('Situação:', '')
        return situation

    #GET LAST EVENT
    
    def get_last_event():
        last_event_in = soupt.find('Último Evento')
        last_event_out = soupt.find('Cartório Extrajudicial:')
        last_event_full = soupt[last_event_in:last_event_out]
        last_event = last_event_full.replace('\n', '').replace('Último Evento', '')
        return last_event

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


    #GET LAWYERS DATA:

    #ADVOGADOS POLO PASSIVO:

    def find_lawpp():
        s_advpp = soup.find(id = 'tabelaAdvogadoPartes29')
        if s_advpp != None:
            advpp_ = s_advpp.get_text()
            advppl = advpp_[20:]
            advpp = advppl.replace('\n', '').replace('  ', '').replace('			 ',' ')
            return advpp
        else:
            s_advppc = soup.find(id = 'tabelaAdvogadoPartes0')
            if s_advppc != None:
                advppc_ = s_advppc.get_text()
                advppce = advppc_[20:]
                advppc = advppce.replace('\n', '').replace('  ', '').replace('			 ',' ')
                return advppc
            else:
                s_advppc = soup.find(id = 'tabelaAdvogadoPartes16')
            if s_advppc != None:
                advppc_ = s_advppc.get_text()
                advppce = advppc_[20:]
                advppc = advppce.replace('\n', '').replace('  ', '').replace('			 ',' ')
                return advppc
            else:
                s_advppc = soup.find(id = 'tabelaAdvogadoPartes67')
            if s_advppc != None:
                advppc_ = s_advppc.get_text()
                advppce = advppc_[20:]
                advppc = advppce..replace('\n', '').replace('  ', '').replace('			 ',' ')

                return advppc
            else:
                return''


    #ADVOGADOS POLO ATIVO:

    def find_lawpa():   
        s_advpa = soup.find(id = 'tabelaAdvogadoPartes30')
        if s_advpa != None:
            advpa_ = s_advpa.get_text()
            advpae = advpa_[20:]
            advpa = advpae..replace('\n', '').replace('  ', '').replace('			 ',' ')
            return advpa
        else:
            s_advpac = soup.find(id = 'tabelaAdvogadoPartes1')
            if s_advpac != None:
                advpac_ = s_advpac.get_text()
                advpace = advpac_[20:]
                advpac = advpace..replace('\n', '').replace('  ', '').replace('			 ',' ')
                return advpac
            else:
                s_advpac = soup.find(id = 'tabelaAdvogadoPartes4')
            if s_advpac != None:
                advpac_ = s_advpac.get_text()
                advpace = advpac_[20:]
                advpac = advpace.replace('\n', '').replace('  ', '').replace('			 ',' ')
                return advpac
            else:
                s_advpac = soup.find(id = 'tabelaAdvogadoPartes14')
            if s_advpac != None:
                advpac_ = s_advpac.get_text()
                advpace = advpac_[20:]
                advpac = advpace.replace('\n', '').replace('  ', '').replace('			 ',' ')
                return advpac
            else:
                return ''


    #GET FOLLOWUP :

    def get_followup():
        andamentos_in = soupt.find('Arquivos/Observação')
        andamentos_out = soupt.find('var ar = document.getElement')
        follow_ups = soupt[andamentos_in:andamentos_out]
        follow_up = follow_ups.replace('\n\n', '').replace('Movimentação sem arquivos', '').replace('Arquivos/Observação',
        'Andamentos:')
        return follow_up

    
    print('Done')

    #STORE LAWSUIT DATA

    lawsuit = {
        'id': get_id(), 
        'judge': find_judge(), 
        'court': get_court(), 
        'date': get_date(),
        'class': get_class(), 
        'subject': get_subject(),
        'phase': get_phase(),
        'situation': get_situation(), 
        'value': get_value(),
        'last event': get_last_event(),
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






