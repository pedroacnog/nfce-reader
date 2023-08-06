import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Pagamento():
    padrao_nfce = r"NFC-e nº: (\d+)"
    padrao_serie = r"Série: (\d+)"
    padrao_data = r"Data de Emissão: (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})"
    padrao_valor_total = r"Valor total R\$\s*([\d,.]+)"
    padrao_valor_descontos = r"Valor descontos R\$\s*([\d,.]+)"
    padrao_valor_pago = r"VALOR PAGO R\$\s*([\d,.]+)"
    padrao_forma_pagamento = r"FORMA PAGAMENTO\s*([\w\s]+)"

    def __init__(self, nfce_cabecalho, nfce_rodape):
        self.nfce_cabecalho = nfce_cabecalho
        self.nfce_rodape = nfce_rodape

    def nfce(self):
        # Realizar a busca usando regex
        nfce_numero = re.search(self.padrao_nfce, self.nfce_cabecalho).group(1)
        serie = re.search(self.padrao_serie, self.nfce_cabecalho).group(1)

        return nfce_numero + serie

    def data_emissao(self):
        data_emissao = re.search(
            self.padrao_data, self.nfce_cabecalho).group(1)

        return data_emissao

    def valor_total(self):
        valor_total = re.search(self.padrao_valor_total,
                                self.nfce_rodape).group(1).replace(',', '.')

        return valor_total

    def descontos(self):
        valor_descontos = re.search(
            self.padrao_valor_descontos, self.nfce_rodape).group(1).replace(',', '.')

        return valor_descontos

    def forma_pagamento(self):
        forma_pagamento = self.nfce_rodape.split()[-2]

        return forma_pagamento

    def valor_pago(self):
        valor_pago = self.nfce_rodape.split()[-1]

        return valor_pago


class Items():

    def __init__(self, nfce_items):
        self.nfce_items = nfce_items


def scraper(param):
    url = f'https://www.sefaz.rs.gov.br/ASP/AAE_ROOT/NFE/SAT-WEB-NFE-NFC_QRCODE_1.asp?p={param}'

    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    table_canhoto = soup.find_all(
        'td', class_='NFCCabecalho_SubTitulo')[2].text

    table_pagamento = soup.find_all('table', class_='NFCCabecalho')[-1].text
    table_items = soup.find_all('table', class_='NFCCabecalho')[-2]

    items = Items(table_items)
    pagamento = Pagamento(table_canhoto, table_pagamento)
    return items, pagamento
