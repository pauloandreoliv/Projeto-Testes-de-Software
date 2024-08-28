import pytest
from google.cloud import firestore
from datetime import datetime, timezone, timedelta
from app import create_pedido, db

@pytest.mark.parametrize("cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now, expected", [
    ("88999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0), 
     {'message': 'Pedido criado com sucesso!'}),

    ("000000000000", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0), 
     {'error': 'CPF inválido!'}),

    ("88999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=1, minute=0, second=0, microsecond=0), 
     {'error': 'Fora do horário de funcionamento (Todos os dias das 8h às 22h)!'}),

    ("88999999999", "", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0), 
     {'error': 'Todos os campos devem ser preenchidos!'}),

    ("88999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "9999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0), 
     {'error': 'Telefone do cliente inválido!'}),
])
def test_create_pedido(cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now, expected):

    result = create_pedido(cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now)
    
    if 'id' in result:
        expected['id'] = result['id']
    
    assert result == expected

    if 'id' in result:
        db.collection('pedido').document(result['id']).delete()

if __name__ == "__main__":
    pytest.main()
