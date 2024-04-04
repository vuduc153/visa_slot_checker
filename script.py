from twocaptcha import TwoCaptcha
import requests
import base64
import os
from io import BytesIO
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


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
        img.save(jpg_buffer, format='JPEG')
        jpg_buffer.seek(0)
        jpg_base64 = base64.b64encode(jpg_buffer.getvalue()).decode()

    return jpg_base64


api_key = os.environ["TWOCAPTCHA_API_KEY"]
in_endpoint = 'https://2captcha.com/in.php'

svg_b64 = b"PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iNTAiIHZpZXdCb3g9IjAsMCwxNTAsNTAiPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9IiNGRkZGRkYiLz48cGF0aCBmaWxsPSIjZGU1Mzc2IiBkPSJNNjUuMDYgMjMuMTlMNjUuMDcgMjMuMjBMNjUuMjIgMjMuMzRRNjQuMjQgMjEuMDkgNjEuOTYgMjAuMTFMNjEuOTYgMjAuMTFRNjAuMDUgMTkuMzAgNTcuMjMgMTkuMzlMNTcuMjMgMTkuMzlMNTcuMjIgMTkuMzhMNTcuMjggMTkuNDVMNTcuMzEgMTkuNDdMNTAuODIgMjAuOTRMNTAuOTQgMjEuMDZMNDguMzkgMjYuNzdMNDguNDcgMjguNzJMNDguNDUgMjguNzBRNDguNDYgMzMuMzEgNTAuOTEgMzUuNTJMNTAuOTEgMzUuNTJRNTMuMTcgMzcuNTQgNTcuNDggMzcuNTRMNTcuNDggMzcuNTRMNTcuNTIgMzcuNTdMNTcuMzggMzcuNDNRNTguNDMgMzcuNDQgNTkuMzQgMzcuMjNMNTkuMzQgMzcuMjNRNjAuMjAgMzcuMDMgNjAuOTIgMzYuNjRMNjAuOTIgMzYuNjRMNjEuMDIgMzYuNzNMNjAuOTkgMzYuNzFMNjEuMDcgMzYuNzlMNjIuNzQgMzMuODlMNjIuNjMgMzMuNzdRNjIuNjIgMzIuNjggNjEuNDEgMzEuOTFMNjEuNDEgMzEuOTFRNjAuNTEgMzEuMzQgNTguOTMgMzAuOTVMNTguOTMgMzAuOTVMNTguOTAgMzAuOTJMNTYuODggMzAuODVMNTYuOTAgMzAuODZMNTYuOTAgMzAuODZRNTYuMzYgMzAuODMgNTUuODQgMzAuODJMNTUuODQgMzAuODJRNTUuMzggMzAuODEgNTQuOTIgMzAuODNMNTQuOTIgMzAuODNMNTQuODYgMzAuNzdMNTQuODcgMzAuNzhRNTQuOTcgMzAuNDkgNTUuMDIgMzAuMDBMNTUuMDIgMzAuMDBRNTUuMDkgMjkuMjkgNTUuMDcgMjguMTZMNTUuMDcgMjguMTZMNTUuMDAgMjguMDlMNTQuODcgMjcuOTZMNTQuOTMgMjguMDJRNTkuMzQgMjcuOTYgNjIuNjAgMjcuODJMNjIuNjAgMjcuODJRNjQuOTMgMjcuNzIgNjYuNjcgMjcuNThMNjYuNjcgMjcuNThMNjYuODMgMjcuNzRMNjYuOTAgMjcuODFMNjYuNzggMjcuNjlRNjYuNzMgMjguMDYgNjYuNzAgMjguNDRMNjYuNzAgMjguNDRRNjYuNjcgMjguODQgNjYuNjcgMjkuMjVMNjYuNjcgMjkuMjVMNjYuODEgMjkuNDBMNjYuNzYgMjkuMzRRNjYuODMgMjkuODEgNjYuODggMzAuMjRMNjYuODggMzAuMjRRNjYuOTMgMzAuNjggNjYuOTQgMzEuMDlMNjYuOTQgMzEuMDlMNjYuNjkgMzAuODNMNjYuNzggMzAuOTJRNjYuMzAgMzAuOTEgNjYuMDMgMzAuOTFMNjYuMDMgMzAuOTFRNjUuNjUgMzAuOTAgNjUuNjUgMzAuOTBMNjUuNjUgMzAuOTBMNjUuNzMgMzAuOThMNjUuNzAgMzAuOTVMNjUuNjcgMzAuOTJMNjQuNTMgMzAuNzdMNjQuNTggMzAuODFRNjUuMzUgMzEuOTAgNjUuODAgMzMuMDJMNjUuODAgMzMuMDJRNjYuMTMgMzMuODMgNjYuMjkgMzQuNjZMNjYuMjkgMzQuNjZMNjYuMjAgMzQuNTdMNjYuMjYgMzQuNjNMNjYuMTQgMzQuNTFRNjYuMTggMzQuODIgNjYuMjEgMzUuMDdMNjYuMjEgMzUuMDdRNjYuMjQgMzUuNDIgNjYuMjQgMzUuNjhMNjYuMjQgMzUuNjhMNjYuMjQgMzUuNjhMNjYuMjMgMzUuNjZMNTcuNDcgNDAuMzRMNTcuNTggNDAuNDZMNTcuNTMgNDAuNDBMNDcuNzYgMzguMjVMNDcuNjkgMzguMThRNDYuODggMzcuMjAgNDYuNDEgMzUuNzNMNDYuNDEgMzUuNzNRNDUuNzkgMzMuNzQgNDUuNzkgMzAuODNMNDUuNzkgMzAuODNMNDUuNzkgMzAuODNMNDUuNzIgMzAuNzZMNDUuNzQgMzAuNzhRNDUuNjggMzAuMTIgNDUuNjEgMjguOTZMNDUuNjEgMjguOTZRNDUuNTUgMjguMDggNDUuNDggMjYuOTFMNDUuNDggMjYuOTFMNDUuNTIgMjYuOTRMNDUuNTUgMjYuOThMNDUuNTIgMjMuMzNMNDUuNDYgMjMuMjdMNDYuOTMgMTguODBMNDcuMDAgMTguODhMNDcuMDMgMTguOTFRNDguNDUgMTcuNjkgNTAuNjMgMTcuMTFMNTAuNjMgMTcuMTFRNTIuMjkgMTYuNjcgNTQuMzkgMTYuNTlMNTQuMzkgMTYuNTlMNTQuNDggMTYuNjhMNTcuMTMgMTYuNTlMNTcuMTAgMTYuNTZMNTcuMTQgMTYuNjBRNTguNzAgMTYuNDYgNjAuNDAgMTYuNTJMNjAuNDAgMTYuNTJRNjEuOTAgMTYuNTcgNjMuNTEgMTYuNzZMNjMuNTEgMTYuNzZMNjMuNTQgMTYuODBMNjMuNjIgMTYuODhMNjMuNTAgMTYuNzZMNjguMzQgMjAuNjBMNjguMzYgMjAuNjNMNjguMjUgMjAuNTJRNjcuNzYgMjAuOTcgNjcuMDEgMjEuNjNMNjcuMDEgMjEuNjNRNjYuMjIgMjIuMzMgNjUuMTQgMjMuMjdMNjUuMTQgMjMuMjdaTTY2LjYzIDI1LjU1TDY2LjYyIDI1LjQ0TDY2Ljc3IDI1LjU4UTY3LjI2IDI1LjA1IDY3LjkwIDI0LjM2TDY3LjkwIDI0LjM2UTY4LjY5IDIzLjUxIDY5LjczIDIyLjQxTDY5LjczIDIyLjQxTDY5Ljc1IDIyLjQzTDY5Ljc2IDIyLjQ0TDY5LjcxIDIyLjQwTDY4LjQzIDE5Ljc0TDY4LjQ5IDE5LjgxUTY3LjgwIDE4LjIzIDY2LjE3IDE3LjM2TDY2LjE3IDE3LjM2UTY1LjA2IDE2Ljc2IDYzLjUxIDE2LjUwTDYzLjUxIDE2LjUwTDYzLjUzIDE2LjUyTDYzLjQ0IDE2LjQzTDYzLjM2IDE2LjM1TDU2Ljk3IDE1Ljk3TDU0LjQzIDE2LjI1TDU0LjI4IDE2LjEwTDQ2LjY2IDE4LjQyTDQ2LjU4IDE4LjM0TDQ1LjE5IDIzLjE1TDQ1LjEzIDIzLjA5TDQ1LjI4IDI4LjA0TDQ1LjM2IDI4LjEyTDQ1LjI4IDI4LjA0TDQ1LjQwIDMyLjE1TDQ1LjQ4IDMyLjIzTDQ3LjMzIDM4LjU0TDQ3LjM3IDM4LjU4UTQ3LjUwIDM4LjkyIDQ3Ljc2IDM5LjI5TDQ3Ljc2IDM5LjI5UTQ4LjA1IDM5LjcyIDQ4LjUyIDQwLjE5TDQ4LjUyIDQwLjE5TDQ4LjY4IDQwLjM1TDQ4LjcyIDQwLjM5TDU2Ljk1IDQyLjQyTDU4LjU1IDQyLjY2TDU5Ljk5IDQyLjc1TDU5Ljg3IDQyLjYzTDYzLjU3IDQyLjcxTDYzLjU3IDQyLjcxUTY0LjQwIDQyLjYzIDY1LjQ4IDQyLjQwTDY1LjQ4IDQyLjQwUTY2LjIxIDQyLjI1IDY3LjA1IDQyLjA0TDY3LjA1IDQyLjA0TDY3LjAxIDQyLjAxTDY3LjE2IDQyLjE1TDY4Ljk4IDM5LjI1TDY4Ljk3IDM5LjI0TDY5LjA5IDM5LjM2UTY5LjA4IDM4Ljc1IDY4LjgzIDM3LjgwTDY4LjgzIDM3LjgwUTY4LjU2IDM2Ljc1IDY4LjAwIDM1LjMwTDY4LjAwIDM1LjMwTDY3LjkxIDM1LjIyTDY3Ljk0IDM1LjI0TDY3LjAyIDMzLjQ1TDY3LjEwIDMzLjUzTDY4Ljg0IDMzLjcxTDY4Ljk2IDMzLjgzUTY4Ljc0IDMxLjgxIDY4LjY2IDMwLjY5TDY4LjY2IDMwLjY5UTY4LjU4IDI5Ljc1IDY4LjYwIDI5LjQzTDY4LjYwIDI5LjQzTDY4LjY1IDI5LjQ4TDY4LjY3IDI5LjUxTDY3Ljg3IDI5LjQ2TDY3Ljg4IDI5LjQ3TDY3Ljg3IDI5LjQ3TDY2Ljk3IDI5LjM2TDY3LjE0IDI5LjUzUTY3LjEyIDI4Ljg5IDY3LjE0IDI4LjI4TDY3LjE0IDI4LjI4UTY3LjE1IDI3LjgwIDY3LjE4IDI3LjMzTDY3LjE4IDI3LjMzTDY3LjE0IDI3LjI5TDY3LjIzIDI3LjM4TDU0LjU2IDI3LjY1TDU0LjU1IDI3LjY0UTU0LjU1IDI4LjE1IDU0LjU1IDI4LjY4TDU0LjU1IDI4LjY4UTU0LjU1IDI5LjA1IDU0LjU1IDI5LjQzTDU0LjU1IDI5LjQzTDU0LjU0IDI5LjQyTDU0LjUyIDMxLjE1TDU0LjU3IDMxLjIwTDU0LjY4IDMxLjMxTDU1LjQwIDMxLjE5TDU1LjM0IDMxLjEzTDU1LjM2IDMxLjE1UTU1LjYxIDMxLjIxIDU1LjgzIDMxLjI0TDU1LjgzIDMxLjI0UTU2LjExIDMxLjI4IDU2LjM2IDMxLjI4TDU2LjM2IDMxLjI4TDU2LjIzIDMxLjE1TDU2LjM4IDMxLjMwTDU2LjQzIDMyLjI2TDU2LjM4IDMyLjIxTDU2LjI1IDMyLjA4TDU2LjM3IDMzLjE5TDU2LjQ2IDMzLjI4TDU2LjM3IDMzLjE5UTU2Ljg1IDMzLjE2IDU3LjMzIDMzLjE0TDU3LjMzIDMzLjE0UTU3Ljg2IDMzLjExIDU4LjQwIDMzLjA5TDU4LjQwIDMzLjA5TDU4LjM0IDMzLjAzTDU4LjMyIDMzLjAwTDYwLjM4IDMzLjA1TDYwLjUwIDMzLjE4TDYyLjM2IDMzLjczTDYyLjM5IDMzLjc4TDYyLjM0IDMzLjc2TDYyLjMyIDMzLjczTDYyLjQxIDMzLjgzUTYyLjU1IDM0Ljc1IDYyLjA3IDM1LjQ0TDYyLjA3IDM1LjQ0UTYxLjcxIDM1Ljk2IDYwLjk5IDM2LjM2TDYwLjk5IDM2LjM2TDYwLjkzIDM2LjMwTDYwLjc2IDM2LjEzTDYwLjc4IDM2LjE1UTU5Ljk2IDM2LjY3IDU5LjEyIDM2LjkyTDU5LjEyIDM2LjkyUTU4LjMxIDM3LjE2IDU3LjQ4IDM3LjE2TDU3LjQ4IDM3LjE2TDU3LjQ1IDM3LjEyTDU3LjQwIDM3LjA4TDUxLjExIDM1LjMxTDUxLjIyIDM1LjQyUTUwLjc2IDM0LjQ3IDUwLjU1IDMzLjQxTDUwLjU1IDMzLjQxUTUwLjMxIDMyLjE5IDUwLjM5IDMwLjgyTDUwLjM5IDMwLjgyTDUwLjM2IDMwLjgwTDUwLjM0IDMwLjc3TDUyLjU0IDI0LjAzTDUyLjQzIDIzLjkzTDUyLjQ3IDIzLjk3TDU5LjE2IDIxLjgyTDU5LjEwIDIxLjc2TDY0Ljc1IDIzLjM4TDY0Ljc1IDIzLjM3TDY0LjYzIDIzLjI1UTY0LjY5IDIzLjMzIDY0Ljc0IDIzLjQxTDY0Ljc0IDIzLjQxUTY0LjgwIDIzLjUwIDY0Ljg2IDIzLjYwTDY0Ljg2IDIzLjYwTDY0Ljg0IDIzLjU4TDY0Ljk0IDIzLjYyTDY1LjAwIDIzLjYyTDY1LjAwIDIzLjYyUTY1LjI3IDIzLjk1IDY1LjU0IDI0LjM4TDY1LjU0IDI0LjM4UTY1Ljg0IDI0LjgzIDY2LjEzIDI1LjQwTDY2LjEzIDI1LjQwTDY2LjA5IDI1LjM2TDY2LjE5IDI1LjI5TDY2LjQ2IDI1LjM4Ii8+PHBhdGggZD0iTTggNDAgQzg2IDQsOTAgMTUsMTM0IDIiIHN0cm9rZT0iIzY5ZTgzZiIgZmlsbD0ibm9uZSIvPjxwYXRoIGZpbGw9IiM1OTk4ZDgiIGQ9Ik04Ni4xOSAxOS43Nkw4Ni4wMSAxOS41OUw4Ni4wMiAxOS42MEw4Ni4wNCAxOS42Mkw4My4wOSAxOS44N0w4My4yMCAxOS45N1E4Mi4zNCAyMC4wMSA4MS42MSAyMC4xNEw4MS42MSAyMC4xNFE4MC44MiAyMC4zMCA4MC4xOSAyMC41N0w4MC4xOSAyMC41N0w4MC4zOCAyMC43N0w4MC4zNyAyMC43NlE3OC44NCAyMS4zOSA3Ny45NSAyMi42NEw3Ny45NSAyMi42NFE3Ni44MSAyNC4yNSA3Ni43NSAyNi44OEw3Ni43NSAyNi44OEw3Ni43OCAyNi45MUw3Ni43MCAyNi44NFE3Ni42OSAyNy45OCA3Ni44MCAyOS4xNkw3Ni44MCAyOS4xNlE3Ni45NSAzMC43OCA3Ny4zMiAzMi40OEw3Ny4zMiAzMi40OEw3Ny4zMiAzMi40OEw3Ny4yMyAzMi4zOUw3Ny4zMyAzMi40OEw4MS44NSAzNy43M0w4MS44NCAzNy43M1E4Mi43MiAzNy45OSA4My40OSAzOC4xMEw4My40OSAzOC4xMFE4NC40MiAzOC4yNCA4NS4yMCAzOC4xNUw4NS4yMCAzOC4xNUw4NS4yMCAzOC4xNUw4NS42MiAzOC4xMUw4NS41OSAzOC4wOEw4NS44NSAzOC4wMEw4NS43NSAzNy45MEw4NS44NCAzNy45OUw4Ni4xNSAzNy45NUw4Ni4xMiAzNy45M0w5MC4yMCAzNy4xN0w4OC4zNyAzNS4zNkw4Ni41OSAzMy42MEw4Ni41NCAzMy41Nkw4Ni42MiAzMy42M1E4Ni43OCAzMy41MCA4Ni45OSAzMy4zMUw4Ni45OSAzMy4zMVE4Ny4yNSAzMy4wNyA4Ny41OSAzMi43M0w4Ny41OSAzMi43M0w4Ny42OCAzMi44Mkw4OC4wOCAzMi4zMUw4OC40OCAzMS43OUw4OC40NSAzMS43N0w4OC41MiAzMS44NFE4OS40NiAzMi45MCA5MC40NSAzMy45N0w5MC40NSAzMy45N1E5MS4zNiAzNC45NSA5Mi4zMSAzNS45M0w5Mi4zMSAzNS45M0w5Mi4zNCAzNS45Nkw5Mi4yMCAzNS44M1E5My41NyAzNC44OSA5NC4yNiAzMi44MUw5NC4yNiAzMi44MVE5NC44MSAzMS4xNSA5NC45MyAyOC43N0w5NC45MyAyOC43N0w5NC44MCAyOC42NEw5NC44NCAyOC42OFE5NC45MCAyOC4yMSA5NC45MyAyNy43Mkw5NC45MyAyNy43MlE5NC45NiAyNy4zMSA5NC45NiAyNi44OUw5NC45NiAyNi44OUw5NC45MyAyNi44N0w5NC45NiAyNi44OUw5NC45MiAyNi44NVE5NC45MCAyMy43NiA5My40MCAyMi4wMkw5My40MCAyMi4wMlE5Mi4xNCAyMC41NiA4OS44MyAyMC4wNUw4OS44MyAyMC4wNUw5MC4wMCAyMC4yM0w5MC4wNyAyMC4yOUw5MC4wMCAyMC4yMlE4OS4xNCAxOS45NCA4Ny45MiAxOS43Nkw4Ny45MiAxOS43NlE4Ny4wNSAxOS42NCA4Ni4wMSAxOS41OEw4Ni4wMSAxOS41OFpNOTguODUgNDEuNzFMOTguOTAgNDEuNzZMOTguNzggNDEuNjRMOTguODYgNDEuNzJMOTcuMDMgNDIuOThMOTIuNjYgMzkuMzJMOTIuNjUgMzkuMzJMODUuOTcgNDAuNjNMODYuMDEgNDAuNjhMODUuOTggNDAuNjRRODIuNjYgNDAuNzcgODAuMzEgNDAuMjNMODAuMzEgNDAuMjNRNzguMTEgMzkuNzMgNzYuNzUgMzguNjVMNzYuNzUgMzguNjVMNzYuNTYgMzguNDZMNzYuNDkgMzguMzlMNzYuNTEgMzguNDFMNzQuMjYgMzMuNjVMNzQuMzYgMzMuNzRMNzMuNzYgMjguMzVMNzMuNzYgMjguMzVMNzMuNTggMjUuODBMNzMuNTYgMjUuNzlRNzMuNDkgMjUuMTMgNzMuNDUgMjQuNjBMNzMuNDUgMjQuNjBRNzMuNDAgMjMuODQgNzMuNDIgMjMuMzJMNzMuNDIgMjMuMzJMNzMuNTIgMjMuNDJMNzMuNTMgMjMuNDRMNzMuNTcgMjMuNDhMNzUuNDggMTguOTFMNzUuMzYgMTguNzlRNzYuMTcgMTguMTMgNzcuNDAgMTcuNjhMNzcuNDAgMTcuNjhRNzguNTcgMTcuMjUgODAuMTMgMTcuMDFMODAuMTMgMTcuMDFMODAuMDcgMTYuOTZMODAuMDUgMTYuOTNMODAuMTQgMTcuMDNMODUuNTYgMTYuNzdMODUuNDkgMTYuNzFRODguNjMgMTYuNzMgOTAuOTkgMTcuMTdMOTAuOTkgMTcuMTdROTQuMjYgMTcuNzYgOTYuMDYgMTkuMTNMOTYuMDYgMTkuMTNMOTYuMTggMTkuMjVMOTYuMTEgMTkuMThMOTYuMTkgMTkuMjZMOTguMDYgMjYuMjdMOTguMDggMjYuMjlROTguMDQgMjguMTIgOTcuOTggMjkuMzdMOTcuOTggMjkuMzdROTcuOTEgMzAuNzAgOTcuODEgMzEuMzlMOTcuODEgMzEuMzlMOTcuNjAgMzEuMTdMOTcuNjMgMzEuMjFMOTcuNTcgMzEuMTRROTcuMzIgMzMuNDAgOTYuNjQgMzUuMTFMOTYuNjQgMzUuMTFROTUuOTMgMzYuOTEgOTQuNzQgMzguMTBMOTQuNzQgMzguMTBMOTQuNjIgMzcuOThMOTQuNTkgMzcuOTRaTTk0LjAwIDE3LjQ1TDk0LjA3IDE3LjUyTDkzLjk3IDE3LjQxTDg1LjQ5IDE2LjI1TDg1LjUwIDE2LjI1TDg1LjQzIDE2LjE5TDgxLjI4IDE2LjMzTDgxLjMxIDE2LjM3TDgxLjI3IDE2LjMzTDc0Ljc3IDE4LjUxTDc0LjgwIDE4LjU0TDczLjExIDIzLjEzTDczLjE5IDIzLjIxUTczLjE2IDIzLjYzIDczLjE5IDI0LjM0TDczLjE5IDI0LjM0UTczLjIxIDI0LjkyIDczLjI4IDI1LjcwTDczLjI4IDI1LjcwTDczLjM5IDI1LjgxTDczLjM4IDI1LjgwUTczLjQ5IDI2Ljc2IDczLjU0IDI3LjQ1TDczLjU0IDI3LjQ1UTczLjU4IDI4LjAzIDczLjU4IDI4LjQzTDczLjU4IDI4LjQzTDczLjQ4IDI4LjMzTDczLjQ5IDI4LjM0TDczLjU2IDI4LjQxUTczLjU3IDI5LjEyIDczLjY1IDMwLjE5TDczLjY1IDMwLjE5UTczLjc1IDMxLjU5IDczLjk3IDMzLjYyTDczLjk3IDMzLjYyTDczLjk0IDMzLjU5TDc0LjAzIDMzLjY4UTc0LjE2IDM1LjIwIDc0LjcxIDM2LjUxTDc0LjcxIDM2LjUxUTc1LjE1IDM3LjU3IDc1Ljg3IDM4LjQ5TDc1Ljg3IDM4LjQ5TDc1Ljk5IDM4LjYxTDc2LjA2IDM4LjY4TDc3LjU3IDQwLjYxTDc3LjQ2IDQwLjQ5TDg1LjUwIDQyLjkxTDg1LjQ3IDQyLjg3TDg1LjQ2IDQyLjg2TDg4LjEyIDQyLjkwTDg4LjI4IDQzLjA2UTkwLjUzIDQzLjA3IDkyLjIyIDQyLjg0TDkyLjIyIDQyLjg0UTk0LjA2IDQyLjU4IDk1LjI0IDQyLjAzTDk1LjI0IDQyLjAzTDk1LjI3IDQyLjA1TDk1LjM4IDQyLjE3TDk1LjM3IDQyLjE1TDEwMC43OSA0Ni4yNEwxMDAuODMgNDYuMjhMMTAwLjkyIDQ2LjM3UTEwMS4xOSA0Ni4xNCAxMDEuNTkgNDUuODFMMTAxLjU5IDQ1LjgxUTEwMi4xMCA0NS40MCAxMDIuODIgNDQuODVMMTAyLjgyIDQ0Ljg1TDEwMi43NiA0NC43OEwxMDIuNzMgNDQuNzZMMTAxLjE3IDQzLjQ5TDEwMC4zMyA0Mi43NUw5OS40NiA0MS45OEw5OS40OSA0MS44Nkw5OS41MSA0MS44OEw5Ny43MCA0MC4zN0w5Ny42OSA0MC4zNkw5Ny42OSA0MC4zNkw5OS42OSAzMy40Mkw5OS43MSAzMy40NEw5OS42OCAzMi4xMUw5OS43NCAzMi4xOEw5OS43OSAzMC45M0w5OS42NSAzMC43OUw5OS42NiAzMC43OVE5OS42OSAyOC4wMCA5OS41MSAyNi4wMUw5OS41MSAyNi4wMVE5OS4zNSAyNC4xMiA5OC45OSAyMi45N0w5OC45OSAyMi45N0w5OS4wMiAyMy4wMEw5OS4xMyAyMy4xMUw5OS4wNSAyMy4wM1E5OC43NyAyMi4yMSA5OC4zNSAyMS41MUw5OC4zNSAyMS41MVE5OC4wNSAyMS4wMCA5Ny42OCAyMC41Nkw5Ny42OCAyMC41Nkw5Ny43MyAyMC42MEw5Ny43NiAyMC42M0w5Ny43MCAyMC41N1E5Ny4yNiAxOS4zNSA5Ni4wNyAxOC40OUw5Ni4wNyAxOC40OVE5NS4yMyAxNy44OSA5NC4wMSAxNy40Nkw5NC4wMSAxNy40NlpNODcuOTAgMjEuOTNMODcuOTUgMjEuOThMODguMDIgMjIuMDVMODguMDUgMjIuMDhROTAuMzkgMjIuMDYgOTEuOTkgMjIuNTdMOTEuOTkgMjIuNTdROTMuMjEgMjIuOTYgOTQuMDAgMjMuNjVMOTQuMDAgMjMuNjVMOTQuMDAgMjMuNjVMOTMuOTkgMjMuNjRMOTMuODkgMjMuNTRROTQuMTkgMjQuMTcgOTQuMzcgMjQuODNMOTQuMzcgMjQuODNROTQuNTQgMjUuNDYgOTQuNTkgMjYuMTFMOTQuNTkgMjYuMTFMOTQuNTQgMjYuMDZMOTQuNTUgMjYuMDdMOTQuNTggMjYuMTBMOTQuNTcgMjguNzFMOTQuNTggMjguNzNMOTIuMzAgMzUuNDBMOTIuMjYgMzUuMzVMOTIuMzQgMzUuNDRMODguNDEgMzEuMjdMODguNTIgMzEuMzhMODYuMTIgMzMuNjJMODYuMTQgMzMuNjVMODYuMjIgMzMuNzJRODYuMzggMzMuOTAgODYuNjkgMzQuMjNMODYuNjkgMzQuMjNRODcuMDkgMzQuNjUgODcuNzMgMzUuMzFMODcuNzMgMzUuMzFMODcuOTAgMzUuNDhMODcuNzEgMzUuNDFMODcuODUgMzUuNTRMODkuMzggMzcuMDhMODkuNDAgMzcuMTBMODkuNDMgMzcuMTNRODkuMDQgMzcuMjcgODguNDEgMzcuNDFMODguNDEgMzcuNDFRODcuNTMgMzcuNjAgODYuMTkgMzcuNzdMODYuMTkgMzcuNzdMODYuMTAgMzcuNjhMODUuODggMzcuNzJMODUuNjEgMzcuNzJMODUuMTggMzcuNzJMODUuMjggMzcuODRMODUuMjAgMzcuNzdMODUuMDcgMzcuNjRRODMuNTggMzcuNjQgODIuMzYgMzcuMzRMODIuMzYgMzcuMzRRODAuNzYgMzYuOTQgNzkuNjMgMzYuMDFMNzkuNjMgMzYuMDFMNzkuNjYgMzYuMDRMNzkuNzEgMzYuMDlRNzkuMjMgMzUuMDggNzguOTkgMzMuODJMNzguOTkgMzMuODJRNzguNzQgMzIuNTEgNzguNzYgMzAuOTFMNzguNzYgMzAuOTFMNzguNTkgMzAuNzRMNzguNjUgMzAuODBMNzguNTggMzAuNzQiLz48cGF0aCBmaWxsPSIjOTY0ZWRlIiBkPSJNMjkuNjIgMzkuODVMMjkuNTQgMzkuNzdMMjkuNjYgMzkuODlMMjkuNjkgMzkuOTJRMjguNzAgMzkuODEgMjcuNzQgMzkuODBMMjcuNzQgMzkuODBRMjYuNjMgMzkuNzggMjUuNTUgMzkuODlMMjUuNTUgMzkuODlMMjUuNTggMzkuOTJMMjUuNjEgMzkuOTVMMjYuMjUgMjkuODZMMjYuMjggMjkuODlMMjYuMjEgMjkuODJMMjUuNzMgMTkuODZMMjUuNjEgMTkuNzRMMjUuNjEgMTkuNzRMMTcuODYgMTcuNzBMMTcuMTcgMTUuOTdMMTcuMTggMTUuOTlMMTcuMTQgMTUuOTVMMTYuNDIgMTQuMzJMMTYuNTEgMTQuNDFMMTYuNDYgMTQuMzVMMjcuNDggMTcuMTVMMjcuNTcgMTcuMjRMMjcuNTIgMTcuMTlRMjkuOTkgMTcuMjIgMzIuNDAgMTYuODdMMzIuNDAgMTYuODdRMzUuNjMgMTYuMzkgMzguNzUgMTUuMjFMMzguNzUgMTUuMjFMMzguNzMgMTUuMTlMMzguNzQgMTUuMjBMMzcuNDQgMTguNTBMMzcuMzggMTguNDRRMzUuNTggMTkuMTQgMzMuNjAgMTkuNTNMMzMuNjAgMTkuNTNRMzEuNjcgMTkuOTEgMjkuNTcgMjAuMDFMMjkuNTcgMjAuMDFMMjkuNjAgMjAuMDNMMjkuNTcgMjAuMDBRMjkuMzQgMjIuNzUgMjkuMjQgMjUuNTVMMjkuMjQgMjUuNTVRMjkuMTYgMjcuNjQgMjkuMTYgMjkuNzZMMjkuMTYgMjkuNzZMMjkuMzQgMjkuOTRMMjkuMzQgMjkuOTRMMjkuMzYgMjkuOTVaTTM5LjUyIDE0LjYxTDM5LjQ0IDE0LjUzTDM5LjUwIDE0LjU5UTM2LjA5IDE1Ljg0IDMyLjU5IDE2LjMxTDMyLjU5IDE2LjMxUTMwLjAwIDE2LjY1IDI3LjM2IDE2LjU3TDI3LjM2IDE2LjU3TDI3LjQwIDE2LjYxTDI3LjMwIDE2LjUyTDI3LjM5IDE2LjYxTDE1LjYxIDEzLjQyTDE1LjYxIDEzLjQzTDE3LjY2IDE3Ljk5TDE3LjczIDE4LjA2TDE5LjU0IDE4Ljg0TDE5LjU2IDE4Ljg2TDE5LjYxIDE4LjkxUTE5LjcyIDE5LjIyIDE5Ljg1IDE5LjY4TDE5Ljg1IDE5LjY4UTIwLjAxIDIwLjI4IDIwLjIxIDIxLjE1TDIwLjIxIDIxLjE1TDIwLjI1IDIxLjE5TDIwLjE5IDIxLjEzTDI1LjU0IDIyLjIyTDI1LjQ3IDIyLjE1TDI1LjUwIDIyLjE3TDI1Ljk5IDI5Ljc1TDI2LjA4IDI5LjgzTDI2LjAxIDI5Ljc2UTI1Ljk3IDMyLjYxIDI1LjcyIDM1LjQ4TDI1LjcyIDM1LjQ4UTI1LjUwIDM3Ljk0IDI1LjEzIDQwLjQyTDI1LjEzIDQwLjQyTDI1LjExIDQwLjQwTDI1LjE5IDQwLjQ4TDI3LjI5IDQwLjI2TDI3LjI4IDQwLjI1TDI3LjI1IDQwLjIyTDI3LjMzIDQxLjMzTDI3LjIyIDQxLjIxTDI3LjE4IDQyLjI0TDI3LjI3IDQyLjM0TDMwLjAwIDQyLjM2TDMwLjA1IDQyLjQxTDI5Ljk1IDQyLjMxUTMwLjUwIDQyLjM3IDMxLjMwIDQyLjQ0TDMxLjMwIDQyLjQ0UTMxLjk1IDQyLjUwIDMyLjc2IDQyLjU3TDMyLjc2IDQyLjU3TDMyLjU5IDQyLjQwTDMyLjc0IDQyLjU1TDMyLjcxIDQyLjUyUTMyLjA4IDQwLjExIDMxLjcyIDM3LjY3TDMxLjcyIDM3LjY3UTMxLjM0IDM1LjAyIDMxLjI4IDMyLjMzTDMxLjI4IDMyLjMzTDMxLjM2IDMyLjQxTDMxLjQxIDMyLjQ2TDMxLjQxIDMyLjQ2UTMxLjM5IDMwLjIyIDMxLjQ4IDI4LjA0TDMxLjQ4IDI4LjA0UTMxLjYwIDI1LjE0IDMxLjkwIDIyLjM0TDMxLjkwIDIyLjM0TDMxLjc2IDIyLjE5TDMxLjc4IDIyLjIxTDMxLjgxIDIyLjI0UTMzLjcxIDIxLjkwIDM1LjQ1IDIxLjQzTDM1LjQ1IDIxLjQzUTM3LjIwIDIwLjk1IDM4Ljc4IDIwLjM0TDM4Ljc4IDIwLjM0TDM4Ljg5IDIwLjQ1TDM4Ljg5IDIwLjQ2TDM4LjkyIDIwLjQ5UTM5LjI0IDE5LjE5IDM5LjY4IDE4LjAwTDM5LjY4IDE4LjAwUTQwLjA3IDE2LjkzIDQwLjU2IDE1Ljk1TDQwLjU2IDE1Ljk1TDQwLjYzIDE2LjAyTDQwLjUxIDE1LjkxTDQwLjU5IDE1Ljk4UTM5Ljc3IDE2LjMxIDM5LjE2IDE2LjU1TDM5LjE2IDE2LjU1UTM4LjcwIDE2LjczIDM4LjM1IDE2Ljg3TDM4LjM1IDE2Ljg3TDM4LjM0IDE2Ljg2TDM4LjI2IDE2Ljc4TDM4LjMxIDE2LjgzUTM4LjY3IDE2LjMyIDM5LjAwIDE1Ljc3TDM5LjAwIDE1Ljc3UTM5LjMxIDE1LjI0IDM5LjU5IDE0LjY4TDM5LjU5IDE0LjY4Ii8+PHBhdGggZD0iTTkgNyBDODMgMzUsODQgNDEsMTM2IDM3IiBzdHJva2U9IiNlYWMwNDIiIGZpbGw9Im5vbmUiLz48cGF0aCBkPSJNMTMgNyBDODUgMjAsOTQgMjAsMTQzIDMxIiBzdHJva2U9IiNlNGU0MzkiIGZpbGw9Im5vbmUiLz48cGF0aCBmaWxsPSIjNWE1YWQ3IiBkPSJNMTI1LjY1IDM0LjcxTDEyNS43MCAzNC43NUwxMjUuNTQgMzQuNTlMMTI1LjU2IDM0LjYyUTEyNS42MSAzNi4yNiAxMjUuMDEgMzcuNDJMMTI1LjAxIDM3LjQyUTEyNC4yNyAzOC44OCAxMjIuNTEgMzkuNjBMMTIyLjUxIDM5LjYwTDEyMi40NyAzOS41NkwxMjIuNTIgMzkuNjFMMTIyLjU4IDM5LjY3UTEyMS4zMiA0MC4wMiAxMTkuMjUgNDAuMjFMMTE5LjI1IDQwLjIxUTExNy44NCA0MC4zNSAxMTYuMDUgNDAuNDFMMTE2LjA1IDQwLjQxTDExNi4xOSA0MC41NUwxMTYuMjIgNDAuNThRMTE0LjE1IDQwLjYwIDExMi41NSA0MC40MEwxMTIuNTUgNDAuNDBRMTEwLjQwIDQwLjEzIDEwOS4xMiAzOS40NUwxMDkuMTIgMzkuNDVMMTA5LjA4IDM5LjQyTDEwOS4wOCAzOS40MUwxMDkuMTMgMzkuNDZRMTA4LjM2IDM4LjkyIDEwNy45NCAzOC4wM0wxMDcuOTQgMzguMDNRMTA3LjMyIDM2Ljc2IDEwNy40MSAzNC43OEwxMDcuNDEgMzQuNzhMMTA3LjQ3IDM0Ljg0TDEwNy41NCAzNC45MEwxMDcuNDMgMzQuODBRMTA3LjUyIDM0LjU3IDEwNy42MCAzNC4wMEwxMDcuNjAgMzQuMDBRMTA3LjcwIDMzLjM4IDEwNy44MCAzMi4zNUwxMDcuODAgMzIuMzVMMTA3LjY1IDMyLjIwTDEwNy41OSAzMi4xNFExMDcuNjUgMzEuNDYgMTA3LjY4IDMwLjg4TDEwNy42OCAzMC44OFExMDcuNzIgMzAuMTIgMTA3LjcyIDI5LjU2TDEwNy43MiAyOS41NkwxMDcuNzEgMjkuNTVMMTA3LjgzIDI5LjY3UTEwNy44MCAyNS4xNCAxMDYuNDYgMjAuODBMMTA2LjQ2IDIwLjgwUTEwNS40MiAxNy40NCAxMDMuNTkgMTQuMjFMMTAzLjU5IDE0LjIxTDEwMy43MCAxNC4zMkwxMDMuNjMgMTQuMjRMMTAzLjY1IDE0LjI3UTEwNC4yMSAxNC41OSAxMDUuMTYgMTUuMDBMMTA1LjE2IDE1LjAwUTEwNi4yMyAxNS40NSAxMDcuODAgMTYuMDJMMTA3LjgwIDE2LjAyTDEwNy42NyAxNS44OEwxMDcuNjggMTUuOTBMMTA3LjgyIDE2LjA0UTEwOS4wNiAxOS4wMiAxMDkuNzMgMjIuMTdMMTA5LjczIDIyLjE3UTExMC41NSAyNS45NiAxMTAuNTUgMzAuMDBMMTEwLjU1IDMwLjAwTDExMC42MyAzMC4wOEwxMTAuNzAgMzAuMTVMMTEwLjU1IDMxLjg4TDExMC40OSAzMS44MkwxMTAuNTAgMzMuNzJMMTEwLjQ2IDMzLjY3UTExMC40NiAzNS4wMCAxMTAuOTggMzUuODlMMTEwLjk4IDM1Ljg5UTExMS4zNiAzNi41MyAxMTIuMDIgMzYuOTVMMTEyLjAyIDM2Ljk1TDExMS45MyAzNi44NkwxMTEuOTcgMzYuOTBMMTEyLjA3IDM3LjAwUTExMi44MyAzNy4zNSAxMTMuOTMgMzcuNTRMMTEzLjkzIDM3LjU0UTExNS4wOCAzNy43MyAxMTYuNjEgMzcuNzNMMTE2LjYxIDM3LjczTDExNi41MSAzNy42M0wxMTYuNjYgMzcuNzhMMTIwLjc2IDM2LjQ0TDEyMC44NiAzNi41NEwxMjAuOTQgMzYuNjJMMTIyLjUwIDMyLjYyTDEyMi42MCAzMi43M0wxMjIuNTIgMzAuMDJMMTIyLjUyIDMwLjAxTDEyNC44OSAxNi40M0wxMjUuOTUgMTYuMTJMMTI3LjExIDE1LjkxTDEyNy4wMCAxNS44MEwxMjYuOTMgMTUuNzNMMTI5LjE5IDE1LjE3TDEyOS4wOCAxNS4wN0wxMjkuMTYgMTUuMTVRMTI3LjM1IDE4LjYzIDEyNi40MiAyMi4yMkwxMjYuNDIgMjIuMjJRMTI1LjQ0IDI1Ljk4IDEyNS40NCAyOS44NUwxMjUuNDQgMjkuODVMMTI1LjQ2IDI5Ljg3TDEyNS40NyAyOS44OEwxMjUuNDQgMjkuODVRMTI1LjQ2IDMwLjI2IDEyNS41MCAzMC44M0wxMjUuNTAgMzAuODNRMTI1LjU0IDMxLjQ5IDEyNS42MSAzMi4zN0wxMjUuNjEgMzIuMzdMMTI1LjU5IDMyLjM0TDEyNS42MCAzMi4zNVpNMTI3Ljc2IDM1LjU2TDEyNy43NyAzNS41N0wxMjcuNzIgMzUuNTJMMTI3LjczIDM1LjUzUTEyNy4yOSAzMi45NiAxMjcuMjcgMzAuMzRMMTI3LjI3IDMwLjM0UTEyNy4yNiAyNy45NSAxMjcuNjEgMjUuNTFMMTI3LjYxIDI1LjUxTDEyNy42NCAyNS41NEwxMjcuNTcgMjUuNDdMMTMwLjgxIDE1Ljk5TDEzMC44NSAxNi4wM1ExMzAuNTEgMTYuMTMgMTMwLjAwIDE2LjMzTDEzMC4wMCAxNi4zM1ExMjkuNDUgMTYuNTQgMTI4LjY5IDE2Ljg4TDEyOC42OSAxNi44OEwxMjguNzggMTYuOTdMMTI4Ljc3IDE2Ljk3TDEyOC44MCAxNi45OUwxMjkuOTQgMTQuNTVMMTI5LjgwIDE0LjQxTDEyOS44MCAxNC40MlExMjguNDAgMTQuOTIgMTI3LjI1IDE1LjI3TDEyNy4yNSAxNS4yN1ExMjUuNTggMTUuNzkgMTI0LjQ1IDE1Ljk5TDEyNC40NSAxNS45OUwxMjQuNTUgMTYuMDlMMTI0LjQ0IDE1Ljk5TDEyNC41MyAxNi4wN0wxMjIuMTUgMjkuODNMMTIyLjIxIDI5LjkwTDEyMi4yMyAzMi42MUwxMjIuMjggMzIuNjdMMTIyLjIwIDMyLjU5UTEyMi4zMyAzMy45NyAxMjEuODMgMzQuOTZMMTIxLjgzIDM0Ljk2UTEyMS40MyAzNS43NSAxMjAuNjQgMzYuMjhMMTIwLjY0IDM2LjI4TDEyMC41OCAzNi4yMkwxMjAuNDkgMzYuMTNMMTE2LjY3IDM3LjQxTDExNi42MCAzNy4zNUwxMTIuNDQgMzYuNjlMMTEyLjM0IDM2LjU4TDExMi4zMiAzNi41N0wxMTIuMjIgMzUuNjdMMTEyLjI5IDM1Ljc0TDExMi4xOSAzNS42NEwxMTIuMzUgMzQuNzNMMTEyLjIwIDM0LjU4TDExMi4yMCAzNC41OEwxMTIuNTIgMzAuMDJMMTEyLjQ0IDI5Ljk1TDExMC45NCAxOC4yNEwxMTAuOTMgMTguMjNMMTA4LjkwIDE3Ljg4TDEwOC43NSAxNy43M0wxMDguNzkgMTcuNzdMMTA4LjAxIDE1LjYxTDEwOC4wNSAxNS42NkwxMDIuOTMgMTMuNTBMMTAyLjgzIDEzLjQxTDEwMi44MSAxMy4zOEwxMDcuNTcgMjkuODRMMTA3LjM5IDI5LjY2TDEwNy40MCAyOS42NkwxMDcuMzkgMzMuMTZMMTA3LjI5IDMzLjA2TDEwNy4xNiAzNi42NkwxMDcuMjAgMzYuNzBMMTA4LjYyIDM5Ljc5TDEwOC41MiAzOS42OUwxMTQuMTcgNDIuNTZMMTE0LjI2IDQyLjY2UTExNS40MCA0Mi43MSAxMTYuNTcgNDIuNzZMMTE2LjU3IDQyLjc2UTExNy40OSA0Mi43OSAxMTguNDMgNDIuODNMMTE4LjQzIDQyLjgzTDExOC40MCA0Mi44MEwxMTguNDEgNDIuODFMMTE4LjQ5IDQyLjg5UTEyMC43MiA0My4wMCAxMjIuNTAgNDIuOTBMMTIyLjUwIDQyLjkwUTEyNS4wNyA0Mi43NiAxMjYuNzEgNDIuMjBMMTI2LjcxIDQyLjIwTDEyNi41NiA0Mi4wNUwxMjYuNjIgNDIuMTFRMTI3LjMzIDQxLjY0IDEyNy43MCA0MC45MkwxMjcuNzAgNDAuOTJRMTI4LjExIDQwLjE0IDEyOC4xMSAzOS4wN0wxMjguMTEgMzkuMDdMMTI4LjExIDM5LjA3TDEyOC4yNSAzOS4yMVExMjguMzAgMzguNzEgMTI4LjIyIDM3Ljg5TDEyOC4yMiAzNy44OVExMjguMTMgMzYuOTkgMTI3Ljg5IDM1LjY5TDEyNy44OSAzNS42OSIvPjwvc3ZnPg=="
jpg_b64 = convert_svg_to_jpg_base64(svg_b64)

solver = TwoCaptcha(api_key)
res = solver.normal(jpg_b64)
print(res)