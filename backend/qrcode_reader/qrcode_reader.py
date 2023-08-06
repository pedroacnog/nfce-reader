import re
import cv2
from pyzbar.pyzbar import decode


def extract_values_from_url(url):
    match = re.search(r'p=(.*)', url)
    if match:
        return match.group(1)
    return None


def QR_Code(image_path):
    image = cv2.imread(image_path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    qr_codes = decode(gray_image)

    if qr_codes:
        qr_data = qr_codes[0].data.decode("utf-8")
        result = extract_values_from_url(qr_data)
        return result
    else:
        return None
