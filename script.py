from twocaptcha import TwoCaptcha
import requests
import base64
import os
from io import BytesIO
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from bs4 import BeautifulSoup
import re


def get_app_id():

    starting_page_url = "https://consulat.gouv.fr/en/ambassade-de-france-en-irlande/appointment?name=Visas"
    
    # Add headers for request authentication
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(starting_page_url, headers=headers)

    # Get the app id from the documen
    pattern = r'"x-gouv-app-id":"([^"]+)"'
    match = re.search(pattern, response.text)

    if match:
        return f'fr.gouv$+{match.group(1)}-meae-ttc'


def get_captcha():

    starting_page_url = "https://consulat.gouv.fr/en/ambassade-de-france-en-irlande/appointment?name=Visas"
    # Add headers for request authentication
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(starting_page_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the element with id "captcha-image"
        captcha = soup.find(id="captcha-image")
        
        if captcha:
            svg_b64 = captcha.get("src").split(",", maxsplit=1)[1]
            # Convert to bytes type
            return svg_b64.encode("ascii")
        else:
            print("Captcha image not found.")
    else:
        print("Failed to retrieve the webpage.")

    return ""
    


def convert_svg_to_jpg_base64(svg_base64):
    # Decode the Base64 SVG image to binary
    svg_data = base64.b64decode(svg_base64)

    # Convert SVG to PIL Image
    drawing = svg2rlg(BytesIO(svg_data))
    img_buffer = BytesIO()
    renderPM.drawToFile(drawing, img_buffer, fmt="JPG")
    img_buffer.seek(0)

    # Convert PIL Image to Base64 JPG
    with Image.open(img_buffer) as img:
        jpg_buffer = BytesIO()
        img.save(jpg_buffer, format="JPEG")
        jpg_buffer.seek(0)
        jpg_base64 = base64.b64encode(jpg_buffer.getvalue()).decode()

    return jpg_base64


if __name__ == '__main__':

    api_key = os.environ["TWOCAPTCHA_API_KEY"]
    svg_b64 = get_captcha()
    jpg_b64 = convert_svg_to_jpg_base64(svg_b64)

    solver = TwoCaptcha(api_key)
    res = solver.normal(jpg_b64)

    print(res)