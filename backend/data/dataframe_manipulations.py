import pandas as pd


def df_pagamento(pagamento):

    dataframe = pd.DataFrame({'id_nfce': pagamento.nfce(),
                              'data_emissao': pagamento.data_emissao(),
                              'valor_total': pagamento.valor_total(),
                              'total_descontos': pagamento.descontos(),
                              'valor_pago': pagamento.valor_pago(),
                              'forma_pagamento': pagamento.forma_pagamento().upper()},
                             index=[0])

    numeric_cols = ['valor_total', 'total_descontos', 'valor_pago']

    dataframe[numeric_cols] = dataframe[numeric_cols].replace(
        ',', '.', regex=True).astype(float)

    dataframe['data_emissao'] = pd.to_datetime(
        dataframe['data_emissao'], format=r'%d/%m/%Y %H:%M:%S')

    return dataframe

# 24/07/2023 14:02:45


def df_items(items):

    df_items = pd.read_html(str(items.nfce_items),
                            header=0, decimal=',', thousands='.')[0]
    return df_items


def join_df(pagamento, items):

    with pd.ExcelWriter("dataframe.xlsx", engine='openpyxl') as writer:
        pagamento.to_excel(writer, sheet_name="Sheet_1")
        items.to_excel(writer, sheet_name="Sheet_1",
                       startcol=7, header=True, index=False)


def nfe_df(items, pagamento):

    pag = df_pagamento(pagamento)
    ite = df_items(items)
    join_df(pag, ite)
