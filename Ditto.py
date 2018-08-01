from bs4 import BeautifulSoup
import re
import urllib3
from splinter import Browser
import json
from urllib.parse import urlencode, urlparse
import requests

with open('law_ids.json') as law_list:
    j = json.load(law_list)


law_ids = []

for i in j['ids']:
    law_ids.append(i) 

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
    #url0 = 'https://projudi.tjba.jus.br/projudi/interno.jsp?endereco=/projudi/buscas/ProcessosParte'
    url1 = 'https://projudi.tjba.jus.br/projudi/listagens/DadosProcesso?numeroProcesso='+idd

    #b = Browser('chrome', headless=True)
    #b.visit(url0)
    #b.visit(url1)
    #data = b.html

    cookies = {
    'JSESSIONID': '6E0926D783832BFA47C2EB13F6C62DED.tomcat61',
} 

    r = requests.post(url1, cookies=cookies)
    data = r.text
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

    #GET DATE

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
        classe = classe_.replace('\n', '').replace('Classe:', '')
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
        fase = faset.replace ('\n', '').replace('      ', ' ').replace('Fase\r  Processual:', '')
        return fase
        
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

    #Passive Pole Parties
    def get_partiespp():
        partes = soup.find(id = 'tabelaPartes29')
        if partes != None:
            partest = partes.get_text()
            partes_polo_passivo = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
            return partes_polo_passivo
        else:
            partes = soup.find(id = 'tabelaPartes0')
            if partes != None:
                partest= partes.get_text()
                partes_polo_passivo = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
                '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
                return partes_polo_passivo
            else:
                partes = soup.find(id = 'tabelaPartes16')
            if partes != None:
                partest= partes.get_text()
                partes_polo_passivo = partest.replace('Não disponível', '').replace('Mostrar/Ocultar', 
                '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
                return partes_polo_passivo
            else:
                return ''

    def get_reu():
        reu_ = soup.find(id = 'tabelaPartes67')
        if reu_ != None:
            reu_t= reu_.get_text()
            reu = reu_t.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
            return reu
        else:
            return ''

    #Active Pole Parties
    def get_partiespa():
        partespa = soup.find(id = 'tabelaPartes30')
        if partespa != None:
            partespa_ = partespa.get_text()
            partes_polo_ativo = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
            return partes_polo_ativo
        else:
            partespa = soup.find(id = 'tabelaPartes1')
            if partespa != None:
                partespa_ = partespa.get_text()
                partes_polo_ativo = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
                '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
                return partes_polo_ativo
            else:
                partespa = soup.find(id = 'tabelaPartes4')
            if partespa != None:
                partespa_ = partespa.get_text()
                partes_polo_ativo = partespa_.replace('Não disponível', '').replace('Mostrar/Ocultar', 
                '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','') 
                return partes_polo_ativo
            else:
                return ''

    def get_autor():
        autor_ = soup.find(id = 'tabelaPartes14')
        if autor_ != None:
            autor_t= autor_.get_text()
            autor = autor_t.replace('Não disponível', '').replace('Mostrar/Ocultar', 
            '').replace('Nome\nIdentidade\nCPF\nAdvogados\nEndereço\n', '').replace('\n', '').replace('\t','').replace('\r','').replace('        ','')
            return autor
        else:
            return ''


    #GET LAWYERS DATA:

    #ADVOGADOS POLO PASSIVO:

    def find_lawpp():
        lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes29')
        if lawyer_raw != None:
            lawyer_text = lawyer_raw.get_text()
            lawyer_text_raw = lawyer_text[20:]
            lawyer_passive = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
            return lawyer_passive
        else:
            lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes0')
            if lawyer_raw != None:
                lawyer_text = lawyer_raw.get_text()
                lawyer_text_raw = lawyer_text[20:]
                lawyer_passive = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
                return lawyer_passive
            else:
                lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes16')
            if lawyer_raw != None:
                lawyer_text = lawyer_raw.get_text()
                lawyer_text_raw = lawyer_text[20:]
                lawyer_passive = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
                return lawyer_passive
            else:
                lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes67')
            if lawyer_raw != None:
                lawyer_text = lawyer_raw.get_text()
                lawyer_text_raw = lawyer_text[20:]
                lawyer_passive = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
                return lawyer_passive
            else:
                return''


    #ADVOGADOS POLO ATIVO:

    def find_lawpa():   
        lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes30')
        if lawyer_raw != None:
            lawyer_text = ss_lawyer.get_text()
            lawyer_text_raw = lawyer_text[20:]
            lawyer_active = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
            return lawyer_active
        else:
            lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes1')
            if lawyer_raw != None:
                lawyer_text = lawyer_raw.get_text()
                lawyer_text_raw = lawyer_text[20:]
                lawyer_active = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
                return lawyer_active
            else:
                lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes4')
            if lawyer_raw != None:
                lawyer_text = lawyer_raw.get_text()
                lawyer_text_raw = lawyer_text[20:]
                lawyer_active = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
                return lawyer_active
            else:
                lawyer_raw = soup.find(id = 'tabelaAdvogadoPartes14')
            if lawyer_raw != None:
                lawyer_text = lawyer_raw.get_text()
                lawyer_text_raw = lawyer_text[20:]
                lawyer_active = lawyer_text_raw.replace('\n', ' ').replace('  ', '').replace('			 ',' ').replace('\t','').replace('\r','')
                return lawyer_active
            else:
                return ''

    #GET FOLLOWUP :

    def get_followup():
        followup = {}
        i = 0
        for td in soup.find_all(size='2'):
            followups = td.next_element
            details_ = followups.next_element.next_element.next_element
            details = str(details_).replace('\r\n', '').replace('                                                                    ', '')
            date_ = details_.next_element.next_element
            datet = str(date_)
            date = datet.replace('<td align="center" nowrap="" width="100">', '').replace('</td>','')
            if date != '\n':
                followup.update({str(i):[date,followups,details]})
                i += 1
        return followup

    
    print('Lawsuit '+get_id()+' acquired')

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
        'lastest event': get_last_event(),
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

    with open(idd+'.json', 'w') as outfile:
        json.dump(lawsuit, outfile, ensure_ascii=False, indent=4)

    del law_ids[0]






