import pytest
from unittest.mock import patch, MagicMock
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase


from app import get_promocao

@pytest.mark.parametrize("prato_id, mock_return, expected", [
    ("1234", MagicMock(exists=True, to_dict=MagicMock(return_value={'nome': 'Pizza Margherita', 'desconto': 10})), {'nome': 'Pizza Margherita', 'desconto': 10}),

    ("", None, {'error': 'ID da promoção deve ser informado!'}),

    ("1234", MagicMock(exists=False), {'error': 'Promoção não encontrada!'}),

    ("1234", Exception("Erro inesperado"), {'error': 'Erro inesperado'}),
])
@patch("app.db.collection")
def test_get_promocao(mock_db_collection, prato_id, mock_return, expected):
    if isinstance(mock_return, MagicMock):
        mock_db_collection.return_value.document.return_value.where.return_value.get.return_value = mock_return
    elif isinstance(mock_return, Exception):
        mock_db_collection.return_value.document.return_value.where.return_value.get.side_effect = mock_return

    result = get_promocao(prato_id)

    assert result == expected

if __name__ == "__main__":
    pytest.main()