from qrcode_reader.qrcode_reader import QR_Code
from web_scraper.web_scraper import scraper
from data.dataframe_manipulations import nfe_df


def main():
    qr_code_reader = QR_Code('backend/img/pedro.png')
    items, pagamento = scraper(qr_code_reader)
    dataframe = nfe_df(items, pagamento)


if __name__ == "__main__":
    main()
