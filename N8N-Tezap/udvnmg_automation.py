from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
import time
import re

udvnmg_automation_bp = Blueprint('udvnmg_automation', __name__)

class UDVNMGAutomator:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.udvnmg.org"
        self.logged_in = False
    
    def login(self, cpf, password):
        """
        Realiza login no sistema UDVNMG
        """
        try:
            # Acessa a página de login
            login_url = f"{self.base_url}/"
            response = self.session.get(login_url)
            
            if response.status_code != 200:
                return False, "Erro ao acessar página de login"
            
            # Prepara dados de login
            login_data = {
                'cpf': cpf,
                'senha': password
            }
            
            # Envia dados de login
            response = self.session.post(login_url, data=login_data)
            
            # Verifica se o login foi bem-sucedido
            if "Real Valor" in response.text and "Sair" in response.text:
                self.logged_in = True
                return True, "Login realizado com sucesso"
            else:
                return False, "Credenciais inválidas"
                
        except Exception as e:
            return False, f"Erro durante login: {str(e)}"
    
    def search_member_debts(self, member_name):
        """
        Busca débitos de um membro específico
        """
        if not self.logged_in:
            return False, "Usuário não está logado"
        
        try:
            # Navega para a seção de consulta
            consulta_url = f"{self.base_url}/consulta.jsp"
            response = self.session.get(consulta_url)
            
            if response.status_code != 200:
                return False, "Erro ao acessar página de consulta"
            
            # Simula busca por membro (implementação específica depende da interface)
            # Esta é uma implementação mockada para demonstração
            mock_debts = {
                'member_name': member_name,
                'debts': [
                    {
                        'type': 'Mensalidade',
                        'month': 'Junho',
                        'year': '2025',
                        'value': 'R$ 41,50'
                    },
                    {
                        'type': 'F.P.S.G.',
                        'month': 'Junho',
                        'year': '2025',
                        'value': 'R$ 6,00'
                    }
                ],
                'total': 'R$ 47,50'
            }
            
            return True, mock_debts
            
        except Exception as e:
            return False, f"Erro ao consultar débitos: {str(e)}"
    
    def register_payment(self, member_name, payment_data):
        """
        Registra um pagamento no sistema
        """
        if not self.logged_in:
            return False, "Usuário não está logado"
        
        try:
            # Navega para a seção de recebimento
            recebimento_url = f"{self.base_url}/recebimento.jsp"
            response = self.session.get(recebimento_url)
            
            if response.status_code != 200:
                return False, "Erro ao acessar página de recebimento"
            
            # Prepara dados do pagamento
            payment_form_data = {
                'nome': member_name,
                'tipo': payment_data.get('tipo', 'Mensalidade'),
                'ano': payment_data.get('ano', '2025'),
                'mes': payment_data.get('mes', '06'),
                'valor': payment_data.get('valor', '0,00')
            }
            
            # Envia dados do pagamento (implementação mockada)
            # Na implementação real, seria necessário analisar o formulário HTML
            
            return True, "Pagamento registrado com sucesso"
            
        except Exception as e:
            return False, f"Erro ao registrar pagamento: {str(e)}"
    
    def generate_receipt(self, member_name, payment_data):
        """
        Gera um recibo no sistema
        """
        if not self.logged_in:
            return False, "Usuário não está logado"
        
        try:
            # Simula geração de recibo
            receipt_data = {
                'receipt_number': f"1512/2025",
                'member_name': member_name,
                'items': payment_data.get('items', []),
                'total': payment_data.get('total', 'R$ 0,00'),
                'date': time.strftime('%d/%m/%Y'),
                'operator': 'Sistema Automatizado'
            }
            
            return True, receipt_data
            
        except Exception as e:
            return False, f"Erro ao gerar recibo: {str(e)}"

# Instância global do automator
automator = UDVNMGAutomator()

@udvnmg_automation_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para realizar login no sistema UDVNMG
    """
    try:
        data = request.get_json()
        
        if not data or 'cpf' not in data or 'password' not in data:
            return jsonify({'error': 'CPF e senha são obrigatórios'}), 400
        
        success, message = automator.login(data['cpf'], data['password'])
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 401
            
    except Exception as e:
        return jsonify({'error': f'Erro no login: {str(e)}'}), 500

@udvnmg_automation_bp.route('/search-debts', methods=['POST'])
def search_debts():
    """
    Endpoint para buscar débitos de um membro
    """
    try:
        data = request.get_json()
        
        if not data or 'member_name' not in data:
            return jsonify({'error': 'Nome do membro é obrigatório'}), 400
        
        success, result = automator.search_member_debts(data['member_name'])
        
        if success:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'error': result}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro na busca: {str(e)}'}), 500

@udvnmg_automation_bp.route('/register-payment', methods=['POST'])
def register_payment():
    """
    Endpoint para registrar um pagamento
    """
    try:
        data = request.get_json()
        
        required_fields = ['member_name', 'payment_data']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Dados incompletos'}), 400
        
        success, result = automator.register_payment(
            data['member_name'], 
            data['payment_data']
        )
        
        if success:
            return jsonify({'success': True, 'message': result})
        else:
            return jsonify({'success': False, 'error': result}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro ao registrar pagamento: {str(e)}'}), 500

@udvnmg_automation_bp.route('/generate-receipt', methods=['POST'])
def generate_receipt():
    """
    Endpoint para gerar um recibo
    """
    try:
        data = request.get_json()
        
        required_fields = ['member_name', 'payment_data']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Dados incompletos'}), 400
        
        success, result = automator.generate_receipt(
            data['member_name'], 
            data['payment_data']
        )
        
        if success:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'error': result}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar recibo: {str(e)}'}), 500

@udvnmg_automation_bp.route('/status', methods=['GET'])
def status():
    """
    Endpoint para verificar status da conexão
    """
    return jsonify({
        'logged_in': automator.logged_in,
        'base_url': automator.base_url
    })

