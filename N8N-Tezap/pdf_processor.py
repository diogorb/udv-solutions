from flask import Blueprint, request, jsonify
import PyPDF2
import re
import io
import base64
from datetime import datetime

pdf_processor_bp = Blueprint('pdf_processor', __name__)

@pdf_processor_bp.route('/process-pdf', methods=['POST'])
def process_pdf():
    """
    Processa um PDF de comprovante de pagamento e extrai informações relevantes
    """
    try:
        # Verifica se um arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Arquivo deve ser um PDF'}), 400
        
        # Lê o conteúdo do PDF
        pdf_content = extract_text_from_pdf(file)
        
        # Extrai informações relevantes
        extracted_data = extract_payment_info(pdf_content)
        
        return jsonify({
            'success': True,
            'data': extracted_data,
            'raw_text': pdf_content
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao processar PDF: {str(e)}'}), 500

def extract_text_from_pdf(file):
    """
    Extrai texto de um arquivo PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")

def extract_payment_info(text):
    """
    Extrai informações específicas do comprovante de pagamento
    """
    extracted_info = {
        'valor': None,
        'cnpj_recebedor': None,
        'nome_recebedor': None,
        'nome_pagador': None,
        'data_transacao': None,
        'tipo_transacao': None,
        'is_valid_cnpj': False
    }
    
    # CNPJ do centro espírita para validação
    CENTRO_ESPIRITA_CNPJ = "07.124.906/0001-67"
    
    # Padrões regex para extração
    patterns = {
        'valor': [
            r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
            r'Valor[:\s]*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
            r'(\d{1,3}(?:\.\d{3})*(?:,\d{2}))\s*R\$'
        ],
        'cnpj': [
            r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})',
            r'CNPJ[:\s]*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})',
            r'(\d{14})'  # CNPJ sem formatação
        ],
        'data': [
            r'(\d{2}/\d{2}/\d{4})',
            r'(\d{2}-\d{2}-\d{4})',
            r'Data[:\s]*(\d{2}/\d{2}/\d{4})'
        ],
        'nome_recebedor': [
            r'Para[:\s]*([A-Z\s]+)',
            r'Recebedor[:\s]*([A-Z\s]+)',
            r'Nome[:\s]*([A-Z\s]+)'
        ],
        'nome_pagador': [
            r'De[:\s]*([A-Z\s]+)',
            r'Pagador[:\s]*([A-Z\s]+)',
            r'Nome[:\s]*([A-Z\s]+)'
        ]
    }
    
    # Extrai valor
    for pattern in patterns['valor']:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_info['valor'] = match.group(1)
            break
    
    # Extrai CNPJs
    cnpjs_found = []
    for pattern in patterns['cnpj']:
        matches = re.findall(pattern, text)
        cnpjs_found.extend(matches)
    
    # Verifica se o CNPJ do centro espírita está presente
    for cnpj in cnpjs_found:
        # Normaliza CNPJ (remove formatação)
        cnpj_normalized = re.sub(r'[^\d]', '', cnpj)
        centro_cnpj_normalized = re.sub(r'[^\d]', '', CENTRO_ESPIRITA_CNPJ)
        
        if cnpj_normalized == centro_cnpj_normalized:
            extracted_info['cnpj_recebedor'] = cnpj
            extracted_info['is_valid_cnpj'] = True
            break
    
    # Extrai data
    for pattern in patterns['data']:
        match = re.search(pattern, text)
        if match:
            extracted_info['data_transacao'] = match.group(1)
            break
    
    # Identifica tipo de transação
    if 'PIX' in text.upper():
        extracted_info['tipo_transacao'] = 'PIX'
    elif 'TED' in text.upper():
        extracted_info['tipo_transacao'] = 'TED'
    elif 'DOC' in text.upper():
        extracted_info['tipo_transacao'] = 'DOC'
    
    # Extrai nomes (lógica mais complexa pode ser necessária)
    if 'ESTRELA DA MANHA' in text.upper():
        extracted_info['nome_recebedor'] = 'ESTRELA DA MANHA'
    
    return extracted_info

@pdf_processor_bp.route('/validate-payment', methods=['POST'])
def validate_payment():
    """
    Valida se um pagamento é válido para o centro espírita
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validações básicas
        validations = {
            'has_value': bool(data.get('valor')),
            'valid_cnpj': data.get('is_valid_cnpj', False),
            'has_date': bool(data.get('data_transacao')),
            'has_payer': bool(data.get('nome_pagador'))
        }
        
        is_valid = all(validations.values())
        
        return jsonify({
            'is_valid': is_valid,
            'validations': validations,
            'message': 'Pagamento válido' if is_valid else 'Pagamento inválido - verifique os dados'
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na validação: {str(e)}'}), 500

