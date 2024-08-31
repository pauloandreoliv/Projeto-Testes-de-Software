import pytest
from unittest.mock import patch, MagicMock
import warnings
warnings.filterwarnings('ignore')  # Ignorar warnings do Firebase

from app import get_pedido, db

def test_get_pedido_valido_com_pedidos():
    cpf = "12345678909"
    pedidos_esperados = [
        {'cpf': cpf, 'endereco': "Rua A", 'formadepgmto': "Cartão", 'pratos': ["Prato2", "Prato3"], 'telefone_cliente': "9999999999", 'total': 50.00, 'data': "15 de August de 2024 às 13:19:22 UTC-3"},
    ]

    with patch('app.validar_cpf', return_value=True):
        with patch('app.db.collection') as mock_db:
            mock_pedidos = MagicMock()
            mock_pedidos.where.return_value.stream.return_value = [MagicMock(to_dict=MagicMock(return_value=pedido)) for pedido in pedidos_esperados]
            mock_db.return_value = mock_pedidos

            resultado = get_pedido(cpf)
            assert resultado == pedidos_esperados

def test_get_pedido_invalido():
    cpf = "00000000000"
    
    with patch('app.validar_cpf', return_value=False):
        resultado = get_pedido(cpf)
        assert resultado == {"error": "CPF inválido!"}

def test_get_pedido_valido_sem_pedidos():
    cpf = "98765432100"
    
    with patch('app.validar_cpf', return_value=True):
        with patch('app.db.collection') as mock_db:
            mock_pedidos = MagicMock()
            mock_pedidos.where.return_value.stream.return_value = []
            mock_db.return_value = mock_pedidos

            resultado = get_pedido(cpf)
            assert resultado == {"error": "Nenhum pedido encontrado para este CPF!"}

def test_get_pedido_erro_inesperado():
    cpf = "12345678909"
    
    with patch('app.validar_cpf', return_value=True):
        with patch('app.db.collection') as mock_db:
            mock_db.side_effect = Exception("Erro Inesperado")
            
            resultado = get_pedido(cpf)
            assert resultado == {"error": "Erro Inesperado"}

if __name__ == "__main__":
    pytest.main()