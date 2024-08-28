import pytest
from unittest.mock import patch, MagicMock
from app import avaliar_pedido

@pytest.mark.parametrize("cpf, pedido_id, nota, mock_pedido_data, expected", [
    ("12345678909", "pedido123", 8.5, 
     MagicMock(exists=True, to_dict=MagicMock(return_value={'cpf': '12345678909'})), 
     {'message': 'Avaliação registrada com sucesso!'}),

    ("00000000000", "pedido123", 8.5, None, 
     {'error': 'CPF inválido!'}),

    ("12345678909", "pedido123", 11, 
     MagicMock(exists=True, to_dict=MagicMock(return_value={'cpf': '12345678909'})), 
     {'error': 'A nota deve ser um valor entre 0 e 10!'}),

    ("12345678909", "pedido999", 8.5, 
     MagicMock(exists=False), 
     {'error': 'Pedido não encontrado!'}),

    ("98765432100", "pedido123", 8.5, 
     MagicMock(exists=True, to_dict=MagicMock(return_value={'cpf': '12345678909'})), 
     {'error': 'CPF não corresponde ao CPF do pedido!'}),
])
@patch("app.db.collection")
@patch("app.validar_cpf")
def test_avaliar_pedido(mock_validar_cpf, mock_db_collection, cpf, pedido_id, nota, mock_pedido_data, expected):
    if cpf == "00000000000":
        mock_validar_cpf.return_value = False
    else:
        mock_validar_cpf.return_value = True

    mock_db_collection.return_value.document.return_value.get.return_value = mock_pedido_data

    result = avaliar_pedido(cpf, pedido_id, nota)
    
    if 'id' in result:
        expected['id'] = result['id']
    
    assert result == expected

if __name__ == "__main__":
    pytest.main()
