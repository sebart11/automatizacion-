from robocorp.tasks import task
import requests
from RPA.Robocorp.Vault import Vault
import re

_secret = Vault().get_secret("ocr2")
endpoint = _secret["url"]
subscription_key = _secret["key"]
image_path = _secret["imagen6"]


@task
def perform_ocr(endpoint, subscription_key, image_path):
    try:
        headers = {
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/octet-stream"
        }
        with open(image_path, 'rb') as image_file:
            data = image_file.read()
            response = requests.post(endpoint, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
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

def extract_text_from_response(response):
    extracted_text = ""
    for region in response["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                extracted_text += word["text"] + " "
            extracted_text += "\n"
    return extracted_text

response = perform_ocr(endpoint, subscription_key, image_path)
if response:
    ocr_text = extract_text_from_response(response)
    cleaned_text = clean_text(ocr_text)
    with open("ocr_result_azure.txt", "w") as file:
        file.write(cleaned_text)
    print("El resultado del OCR se ha guardado en 'ocr_result_azure.txt'.")
else:
    print("No se pudo obtener el resultado del OCR.")       

    
    