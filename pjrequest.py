import requests
from bs4 import BeautifulSoup
import json

url = 'https://projudi.tjba.jus.br/projudi/buscas/ProcessosParte' 

cookies = {
    'JSESSIONID': '6F89E08CC84C31A8D8156CC90114A31E.tomcat21',
} 

page = 1

data = [
  ('nome', ''),
  ('cpfCnpj', ''),
  ('sentencaInteira', ''),
  ('tipoParteProcesso', '-1'),
  ('codVara', '-1'),
  ('numeroProcesso', ''),
  ('codObjetoPedido', '-1'),
  ('codFaseProcessual', '-1'),
  ('tipoAcao', '-1'),
  ('codPrioridadeProcessual', '-1'),
  ('codStatusProcesso', '-1'),
  ('codNatureza', '-1'),
  ('segredo', ''),
  ('vinculado', ''),
  ('codTipoLocalizador', ''),
  ('codSituacao', '-1'),
  ('dataInicio', ''),
  ('dataFim', ''),
  ('loginJuiz', ''),
  ('codCartorioExtrajudicial', ''),
  ('codNucleoMP', ''),
  ('seqCategoriaClasse', ''),
  ('pesquisaRecursivaClasse', ''),
  ('seqCategoriaAssunto', ''),
  ('pesquisaRecursivaAssunto', ''),
  ('dataFato', ''),
  ('delegaciaOrigem', '-1'),
  ('numeroProcessoTCO', ''),
  ('dataTCO', ''),
  ('codTipoRegistroOcorrencia', '-1'),
  ('tipoRegistroOutros', ''),
  ('numeroRegistro', ''),
  ('oab', ''),
  ('complementoOAB', ''),
  ('estadoOAB', ''),
  ('migradoSaipro', ''),
  ('pagina', str(page)),
  ('coluna', 'Processo.DATARECEBIMENTO'),
  ('ordem', 'DESC'),
]


law_ids = {
    'ids':[

    ]
}
law_num = []
index=0

while (page <= 20):
    r = requests.post(url, cookies=cookies, data=data)
    pag = r.text
    soup = BeautifulSoup(pag, 'html.parser')

    for link in soup.find_all('a', 'style2'):
        law_ids['ids'].append(link.get('href')[48:])
    page = page+1
    index += 1
    data[36] = ('pagina', str(page))
    print(page)

 

with open('law_ids.json', 'w') as outfile:
        json.dump(law_ids, outfile, indent=4)

print('Done!')
