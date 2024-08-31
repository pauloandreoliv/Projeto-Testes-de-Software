import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from app import create_pedido
import warnings
warnings.filterwarnings('ignore')

def mock_validar_cpf(cpf):
    return cpf != "00000000000"

@pytest.mark.parametrize("cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now, side_effect, expected", [
    ("88999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0),
     None, {'message': 'Pedido criado com sucesso!'}),

    ("000000000000", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0),
     None, {'error': 'CPF inválido!'}),

    ("88999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=1, minute=0, second=0, microsecond=0),
     None, {'error': 'Fora do horário de funcionamento (Todos os dias das 8h às 22h)!'}),

    ("88999999999", "", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0),
     None, {'error': 'Todos os campos devem ser preenchidos!'}),

    ("88999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "9999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0),
     None, {'error': 'Telefone do cliente inválido!'}),

    ("88999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0),
     Exception("Erro Inesperado"), {'error': 'Erro Inesperado'}),
     
    ("19999999999", "Rua B, 456", "Cartão", ["Prato1", "Prato2"], "81999999999", 59.9, datetime.now(timezone.utc).replace(hour=13, minute=0, second=0, microsecond=0),
     None, {'error': 'Nenhum usuário encontrado com este CPF!'}),
])
@patch('app.db.collection')
def test_create_pedido(mock_db_collection, cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now, side_effect, expected):
    if mock_validar_cpf(cpf) is True:
        mock_usuario_ref = MagicMock()
        mock_pedido_ref = MagicMock()
        mock_db_collection.return_value.add.return_value = (None, mock_usuario_ref)
        if cpf == "19999999999":
            mock_db_collection.return_value.where.return_value.stream.return_value = []
        else:
            mock_db_collection.return_value.where.return_value.stream.return_value = [mock_pedido_ref]
        
        if side_effect:
            mock_db_collection.return_value.where.side_effect = side_effect
    result = create_pedido(cpf, endereco, formadepgmto, pratos, telefone_cliente, total, now)
    if 'message' in expected:
        assert 'id' in result
        expected['id'] = result['id']
        
    assert result == expected

if __name__ == "__main__":
    pytest.main()