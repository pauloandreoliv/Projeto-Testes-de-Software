import pytest
from unittest.mock import patch, MagicMock

from app import get_prato

@pytest.mark.parametrize("prato_id, mock_return, expected", [
    ("1234", MagicMock(exists=True, to_dict=MagicMock(return_value={'nome': 'Pizza Margherita', 'preco': 35})), {'nome': 'Pizza Margherita', 'preco': 35}),

    ("", None, {'error': 'ID do prato deve ser informado!'}),

    ("9999", MagicMock(exists=False), {'error': 'Prato não encontrado!'}),

    ("1234", Exception("Erro inesperado"), {'error': 'Erro inesperado'}),
])
@patch("app.db.collection")
def test_get_prato(mock_db_collection, prato_id, mock_return, expected):
    if isinstance(mock_return, MagicMock):
        mock_db_collection.return_value.document.return_value.get.return_value = mock_return
    elif isinstance(mock_return, Exception):
        mock_db_collection.return_value.document.return_value.get.side_effect = mock_return

    result = get_prato(prato_id)

    assert result == expected

if __name__ == "__main__":
    pytest.main()