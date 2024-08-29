import pytest
from google.cloud import firestore
from unittest.mock import patch
from datetime import datetime, timezone
from app import create_pedido, db
import warnings
warnings.filterwarnings('ignore') 

def mock_validar_cpf(cpf):
    return cpf != "00000000000"

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
    if mock_validar_cpf(cpf) is True:
        doc_ref = db.collection('usuario').add({
                'cpf': cpf
            })

        pedido_ref = db.collection('pedido').where('cpf', '==', cpf).stream()
        for pedido in pedido_ref:
            pedido.reference.delete()

    result = create_pedido(cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now)
    
    if 'message' in expected:
        assert 'id' in result
        expected['id'] = result['id']
        
        pedido_ref = db.collection('pedido').document(result['id'])
        pedido_data = pedido_ref.get().to_dict()
        assert pedido_data is not None
        
    assert result == expected
    
    if mock_validar_cpf(cpf) is True:
        usuario_ref = db.collection('usuario').where('cpf', '==', cpf).stream()
        for usuario in usuario_ref:
            usuario.reference.delete()

        pedido_ref = db.collection('pedido').where('cpf', '==', cpf).stream()
        for pedido in pedido_ref:
            pedido.reference.delete()

if __name__ == "__main__":
    pytest.main()
