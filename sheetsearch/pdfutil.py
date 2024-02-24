from datetime import datetime
import os
import random
import string
from PIL import Image
from fpdf import FPDF
import requests
import magic


def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # 에러가 발생하면 예외를 발생시킵니다.

    mime_type = magic.from_buffer(response.content, mime=True)

    # 확장자 결정
    if mime_type == 'image/jpeg':
        ext = '.jpg'
    elif mime_type == 'image/png':
        ext = '.png'
    elif mime_type == 'image/gif':
        ext = '.gif'
    # elif mime_type == 'image/svg+xml':
        # ext = '.svg'
    else:
        raise ValueError('Unknown MIME type: ' + mime_type)

    # 확장자 추가
    filename += ext

    with open(filename, 'wb') as f:
        f.write(response.content)

    return filename


def random_text(length=12):
    chars = string.ascii_letters + string.digits
    random_text = "".join(random.choice(chars) for _ in range(length))
    return random_text


def download_imagefiles(image_urls, download_dir):
    image_files = []
    for image_url in image_urls:
        filename = os.path.join(download_dir, random_text())
        output_name = download_file(image_url, filename)
        image_files.append(output_name)

    return image_files


def generate_pdf(img_files, target_dir):
    pdf_width = 595
    pdf_height = 842

    margin_vertical = 20
    margin_horizontal = 20

    inner_width = pdf_width - 2 * margin_horizontal
    inner_height = pdf_height - 2 * margin_vertical

    pdf = FPDF(unit="pt", format=[595, 842])

    for img_file in img_files:
        img_path = img_file
        img = Image.open(img_path)
        orig_width, orig_height = img.size

        width_ratio = inner_width / orig_width
        height_ratio = inner_height / orig_height

        if width_ratio < height_ratio:
            new_width = inner_width
            new_height = int(width_ratio * orig_height)
        else:
            new_width = int(height_ratio * orig_width)
            new_height = inner_height

        img = img.resize((new_width, new_height))

        x = (pdf_width - new_width) / 2
        y = (pdf_height - new_height) / 2

        pdf.add_page()
        pdf.image(img_path, x, y, new_width, new_height)


    output_filename = os.path.join(target_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

    pdf.output(output_filename)

    return output_filename


