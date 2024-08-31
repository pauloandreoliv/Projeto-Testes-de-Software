import pytest
from unittest.mock import patch, MagicMock
from app import avaliar_pedido
import warnings 
warnings.filterwarnings('ignore')  # Ignorar warning do firebase


@pytest.mark.parametrize("cpf, pedido_id, nota, mock_pedido_data, side_effect, expected", [
    ("12345678909", "pedido123", 8.5, 
     MagicMock(exists=True, to_dict=MagicMock(return_value={'cpf': '12345678909'})), 
     None,
     {'message': 'Avaliação registrada com sucesso!'}),

    ("00000000000", "pedido123", 8.5, None, 
     None,
     {'error': 'CPF inválido!'}),

    ("12345678909", "pedido123", 11, 
     MagicMock(exists=True, to_dict=MagicMock(return_value={'cpf': '12345678909'})), 
     None,
     {'error': 'A nota deve ser um valor entre 0 e 10!'}),

    ("12345678909", "pedido999", 8.5, 
     MagicMock(exists=False), 
     None,
     {'error': 'Pedido não encontrado!'}),

    ("98765432100", "pedido123", 8.5, 
     MagicMock(exists=True, to_dict=MagicMock(return_value={'cpf': '12345678909'})), 
     None,
     {'error': 'CPF não corresponde ao CPF do pedido!'}),

    ("12345678909", "pedido123", 8.5, 
     MagicMock(exists=True, to_dict=MagicMock(return_value={'cpf': '12345678909'})), 
     Exception("Erro Inesperado"),
     {'error': 'Erro Inesperado'}),
])
@patch("app.db.collection")
@patch("app.validar_cpf")
def test_avaliar_pedido(mock_validar_cpf, mock_db_collection, cpf, pedido_id, nota, mock_pedido_data, side_effect, expected):
    if cpf == "00000000000":
        mock_validar_cpf.return_value = False
    else:
        mock_validar_cpf.return_value = True

    mock_doc = mock_db_collection.return_value.document.return_value.get
    mock_doc.return_value = mock_pedido_data

    if side_effect:
        mock_doc.side_effect = side_effect

    result = avaliar_pedido(cpf, pedido_id, nota)
    
    if 'id' in result:
        expected['id'] = result['id']
    
    assert result == expected

if __name__ == "__main__":
    pytest.main()