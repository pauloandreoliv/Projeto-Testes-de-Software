import pytest
from unittest.mock import patch, MagicMock
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase

from app import get_pedido, validar_cpf, db

def test_get_pedido_valido_com_pedidos():
    cpf = "12345678909"
    pedidos_esperados = [
        {'cpf': cpf, 'endereco': "Rua A", 'formadepgmto': "Cartão", 'pratos': ["Prato2", "Prato3"], 'telefone_cliente': "9999999999", 'total': 50.00, 'data': "15 de August de 2024 às 13:19:22 UTC-3"},
    ]

    pedidos_collection = db.collection('pedido')
    for pedido in pedidos_esperados:
        pedidos_collection.add(pedido)

    with patch('app.validar_cpf', return_value=True):
        resultado = get_pedido(cpf)
        assert resultado == pedidos_esperados

    docs = pedidos_collection.where('cpf', '==', cpf).stream()
    for doc in docs:
        doc.reference.delete()

def test_get_pedido_invalido():
    cpf = "00000000000"
    
    with patch('app.validar_cpf', return_value=False):
        resultado = get_pedido(cpf)
        assert resultado == {"error": "CPF inválido!"}

def test_get_pedido_valido_sem_pedidos():
    cpf = "98765432100"
    
    with patch('app.validar_cpf', return_value=True):
        with patch('app.get_pedido', return_value=[]):
            resultado = get_pedido(cpf)
            assert resultado == {"error": "Nenhum pedido encontrado para este CPF!"}

def test_get_pedido_erro_inesperado():
    cpf = "12345678909"
    
    with patch('app.validar_cpf', return_value=True):
        with patch('app.db.collection') as mock_db:
            mock_db.side_effect = Exception("Erro de conexão")
            
            resultado = get_pedido(cpf)
            assert resultado == {"error": "Erro de conexão"}

if __name__ == "__main__":
    pytest.main()