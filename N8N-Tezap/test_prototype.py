#!/usr/bin/env python3
"""
Script de teste para demonstrar as funcionalidades do protótipo
"""

import requests
import json
import base64
import os

# URL base da API
BASE_URL = "http://localhost:5001/api"

def test_pdf_processing():
    """
    Testa o processamento de PDF
    """
    print("=== Teste de Processamento de PDF ===")
    
    # Simula upload de PDF
    pdf_path = "/home/ubuntu/upload/ValJunho.pdf"
    
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            try:
                response = requests.post(f"{BASE_URL}/pdf/process-pdf", files=files, timeout=10)
                print(f"Status: {response.status_code}")
                print(f"Resposta: {response.json()}")
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}")
    else:
        print("Arquivo PDF não encontrado")

def test_udvnmg_status():
    """
    Testa o status da conexão com UDVNMG
    """
    print("\n=== Teste de Status UDVNMG ===")
    
    try:
        response = requests.get(f"{BASE_URL}/udvnmg/status", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

def test_whatsapp_webhook():
    """
    Testa o webhook do WhatsApp
    """
    print("\n=== Teste de Webhook WhatsApp ===")
    
    # Simula verificação de webhook
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': 'your_webhook_token_here',
        'hub.challenge': 'test_challenge'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/whatsapp/webhook", params=params, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

def test_message_processing():
    """
    Testa o processamento de mensagens
    """
    print("\n=== Teste de Processamento de Mensagens ===")
    
    # Simula mensagem do WhatsApp
    message_data = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "5511999999999",
                        "type": "text",
                        "text": {
                            "body": "Consultar débitos João Silva"
                        }
                    }]
                }
            }]
        }]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/whatsapp/webhook", 
                               json=message_data, 
                               timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

def main():
    """
    Executa todos os testes
    """
    print("Iniciando testes do protótipo...")
    
    test_udvnmg_status()
    test_whatsapp_webhook()
    test_message_processing()
    test_pdf_processing()
    
    print("\nTestes concluídos!")

if __name__ == "__main__":
    main()

