from flask import Blueprint, request, jsonify
import base64
import io
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

whatsapp_integration_bp = Blueprint('whatsapp_integration', __name__)

class WhatsAppHandler:
    def __init__(self):
        self.webhook_token = "your_webhook_token_here"
        self.access_token = "your_access_token_here"
    
    def verify_webhook(self, mode, token, challenge):
        """
        Verifica webhook do WhatsApp Business API
        """
        if mode == "subscribe" and token == self.webhook_token:
            return challenge
        return None
    
    def process_message(self, message_data):
        """
        Processa mensagem recebida do WhatsApp
        """
        try:
            # Extrai informações da mensagem
            from_number = message_data.get('from')
            message_type = message_data.get('type')
            
            if message_type == 'text':
                text_content = message_data.get('text', {}).get('body', '')
                return self.handle_text_message(from_number, text_content)
            
            elif message_type == 'document':
                document_data = message_data.get('document', {})
                return self.handle_document_message(from_number, document_data)
            
            else:
                return {
                    'type': 'text',
                    'content': 'Tipo de mensagem não suportado. Envie texto ou PDF.'
                }
                
        except Exception as e:
            return {
                'type': 'text',
                'content': f'Erro ao processar mensagem: {str(e)}'
            }
    
    def handle_text_message(self, from_number, text):
        """
        Processa mensagens de texto
        """
        text_lower = text.lower()
        
        # Comando para consultar débitos
        if 'consultar' in text_lower or 'debitos' in text_lower:
            # Extrai nome da mensagem
            name = self.extract_name_from_text(text)
            if name:
                return {
                    'type': 'debt_query',
                    'member_name': name,
                    'content': f'Consultando débitos para {name}...'
                }
            else:
                return {
                    'type': 'text',
                    'content': 'Por favor, informe o nome para consulta. Exemplo: "Consultar débitos João Silva"'
                }
        
        # Comando para emitir recibo
        elif 'recibo' in text_lower or 'emitir' in text_lower:
            return {
                'type': 'text',
                'content': 'Para emitir recibo, envie o comprovante de pagamento em PDF.'
            }
        
        # Comando de ajuda
        elif 'ajuda' in text_lower or 'help' in text_lower:
            return {
                'type': 'text',
                'content': self.get_help_message()
            }
        
        else:
            return {
                'type': 'text',
                'content': 'Comando não reconhecido. Digite "ajuda" para ver os comandos disponíveis.'
            }
    
    def handle_document_message(self, from_number, document_data):
        """
        Processa documentos enviados
        """
        mime_type = document_data.get('mime_type', '')
        
        if mime_type == 'application/pdf':
            return {
                'type': 'pdf_processing',
                'document_id': document_data.get('id'),
                'content': 'Processando comprovante de pagamento...'
            }
        else:
            return {
                'type': 'text',
                'content': 'Apenas arquivos PDF são aceitos para comprovantes de pagamento.'
            }
    
    def extract_name_from_text(self, text):
        """
        Extrai nome da mensagem de texto
        """
        # Remove palavras de comando
        words_to_remove = ['consultar', 'debitos', 'débitos', 'para', 'de', 'do', 'da']
        words = text.split()
        
        filtered_words = []
        for word in words:
            if word.lower() not in words_to_remove:
                filtered_words.append(word)
        
        if len(filtered_words) >= 2:
            return ' '.join(filtered_words).title()
        
        return None
    
    def get_help_message(self):
        """
        Retorna mensagem de ajuda
        """
        return """
🤖 *Assistente do Centro Espírita*

*Comandos disponíveis:*

📋 *Consultar débitos:*
"Consultar débitos [Nome]"
Exemplo: "Consultar débitos João Silva"

💰 *Processar pagamento:*
Envie o comprovante de pagamento em PDF

❓ *Ajuda:*
Digite "ajuda" para ver esta mensagem

---
Para dúvidas, entre em contato com a tesouraria.
        """
    
    def create_receipt_image(self, receipt_data):
        """
        Cria uma imagem do recibo (simulação)
        """
        try:
            # Cria uma imagem em branco
            width, height = 800, 600
            image = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(image)
            
            # Tenta carregar uma fonte (usa fonte padrão se não encontrar)
            try:
                font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                font_normal = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            except:
                font_title = ImageFont.load_default()
                font_normal = ImageFont.load_default()
            
            # Desenha o cabeçalho
            y_position = 50
            draw.text((50, y_position), "Centro Espírita Beneficente União do Vegetal", 
                     fill='black', font=font_title)
            y_position += 30
            draw.text((50, y_position), "Estrela da Manhã - 4ª Região", 
                     fill='black', font=font_normal)
            y_position += 20
            draw.text((50, y_position), "07.124.906/0001-67", 
                     fill='black', font=font_normal)
            
            # Desenha linha separadora
            y_position += 40
            draw.line([(50, y_position), (width-50, y_position)], fill='black', width=2)
            
            # Título do recibo
            y_position += 30
            draw.text((width//2-50, y_position), "RECIBO", 
                     fill='black', font=font_title)
            
            # Dados do recibo
            y_position += 50
            draw.text((50, y_position), f"Recibo Nº: {receipt_data.get('receipt_number', 'N/A')}", 
                     fill='black', font=font_normal)
            y_position += 25
            draw.text((50, y_position), f"Jr.: {receipt_data.get('member_name', 'N/A')}", 
                     fill='black', font=font_normal)
            
            # Itens do recibo
            y_position += 40
            for item in receipt_data.get('items', []):
                draw.text((50, y_position), f"{item.get('description', '')} - {item.get('value', '')}", 
                         fill='black', font=font_normal)
                y_position += 20
            
            # Total
            y_position += 20
            draw.text((50, y_position), f"Total do Recibo: {receipt_data.get('total', 'R$ 0,00')}", 
                     fill='black', font=font_title)
            
            # Data e operador
            y_position += 50
            draw.text((50, y_position), f"Tesouraria em: {receipt_data.get('date', '')}", 
                     fill='black', font=font_normal)
            y_position += 20
            draw.text((50, y_position), f"Emitido por: {receipt_data.get('operator', '')}", 
                     fill='black', font=font_normal)
            
            # Converte para base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            
            return base64.b64encode(buffer.getvalue()).decode()
            
        except Exception as e:
            raise Exception(f"Erro ao criar imagem do recibo: {str(e)}")

# Instância global do handler
whatsapp_handler = WhatsAppHandler()

@whatsapp_integration_bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Endpoint webhook para WhatsApp Business API
    """
    if request.method == 'GET':
        # Verificação do webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        verification = whatsapp_handler.verify_webhook(mode, token, challenge)
        if verification:
            return verification
        else:
            return 'Forbidden', 403
    
    elif request.method == 'POST':
        # Processamento de mensagens
        try:
            data = request.get_json()
            
            # Extrai dados da mensagem
            entry = data.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            messages = value.get('messages', [])
            
            if messages:
                message = messages[0]
                response = whatsapp_handler.process_message(message)
                
                # Aqui você integraria com a API do WhatsApp para enviar resposta
                # Por enquanto, apenas retorna a resposta processada
                return jsonify({'success': True, 'response': response})
            
            return jsonify({'success': True, 'message': 'No messages to process'})
            
        except Exception as e:
            return jsonify({'error': f'Erro no webhook: {str(e)}'}), 500

@whatsapp_integration_bp.route('/send-message', methods=['POST'])
def send_message():
    """
    Endpoint para enviar mensagem via WhatsApp (simulação)
    """
    try:
        data = request.get_json()
        
        required_fields = ['to', 'message']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Campos obrigatórios: to, message'}), 400
        
        # Simula envio de mensagem
        return jsonify({
            'success': True,
            'message_id': f"msg_{datetime.now().timestamp()}",
            'to': data['to'],
            'content': data['message']
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao enviar mensagem: {str(e)}'}), 500

@whatsapp_integration_bp.route('/send-image', methods=['POST'])
def send_image():
    """
    Endpoint para enviar imagem via WhatsApp (simulação)
    """
    try:
        data = request.get_json()
        
        required_fields = ['to', 'image_base64']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Campos obrigatórios: to, image_base64'}), 400
        
        # Simula envio de imagem
        return jsonify({
            'success': True,
            'message_id': f"img_{datetime.now().timestamp()}",
            'to': data['to'],
            'type': 'image'
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao enviar imagem: {str(e)}'}), 500

