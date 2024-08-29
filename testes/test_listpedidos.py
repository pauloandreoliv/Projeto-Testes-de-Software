import pytest
from unittest.mock import patch, MagicMock
from app import list_pedidos
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase


@pytest.mark.parametrize("permissao, mock_pedidos, expected", [
    ("ATENDENTE", [MagicMock(id='pedido1', to_dict=lambda: {'cpf': '12345678909', 'total': 50.0}),
                   MagicMock(id='pedido2', to_dict=lambda: {'cpf': '98765432100', 'total': 75.0})],
     [{'id': 'pedido1', 'cpf': '12345678909', 'total': 50.0}, {'id': 'pedido2', 'cpf': '98765432100', 'total': 75.0}]),
    
    ("COZINHEIRO", None, {'error': 'Nível de permissão inválido!'}),
    
    ("GERENTE", [], {'error': 'Nenhum pedido encontrado!'}),
])
@patch('app.db.collection')
def test_list_pedidos(mock_db_collection, permissao, mock_pedidos, expected):

    if mock_pedidos is not None:
        mock_collection = mock_db_collection.return_value
        mock_collection.stream.return_value = mock_pedidos

    resultado = list_pedidos(permissao)
    assert resultado == expected
    
    if permissao.upper().strip() in ['ATENDENTE', 'GERENTE']:
        mock_db_collection.assert_called_once_with('pedido')
        mock_db_collection.return_value.stream.assert_called_once()

if __name__ == "__main__":
    pytest.main()
