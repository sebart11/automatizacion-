from robocorp.tasks import task
import requests
import os
from RPA.Robocorp.Vault import Vault
import re

_secret = Vault().get_secret("ocr")
api_url = _secret["url"]
api_key = _secret["key"]
image_path = _secret["imagen"]

@task
def perform_ocr(api_url, api_key, image_path):
    try:
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            headers = {'apikey': api_key}
            response = requests.post(api_url, files=files, headers=headers)
            if response.status_code == 200:
                # Extraer solo el texto de la respuesta JSON
                ocr_text = response.json()["ParsedResults"][0]["ParsedText"]
                return ocr_text
            else:
                print(f"Error en la solicitud: {response.status_code}")
                return None
    except Exception as e:
        print(f"Se produjo un error: {e}")
        return None
def clean_text(text):
    # Eliminar saltos de línea y espacios innecesarios
    text = re.sub(r'\r\n+', '\n', text)
    text = re.sub(r'\n{2,}', '\n', text)
    # Eliminar caracteres especiales
    text = re.sub(r'[^\w\s\n]', '', text)
    # Convertir letras mayúsculas a minúsculas
    text = text.lower()
    return text

    
ocr_result = perform_ocr(api_url, api_key, image_path)


if ocr_result:
    with open("ocr_result.txt", "w") as file:
        file.write(str(ocr_result))
    print("El resultado del OCR se ha guardado en 'ocr_result.txt'.")
else:
    print("No se pudo obtener el resultado del OCR.")

