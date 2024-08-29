import pytest
from unittest.mock import patch, MagicMock
from app import create_promocao
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase


@pytest.mark.parametrize("prato_id, promocao, permissao, prato_exists, expected", [
    ("1234", True, "GERENTE", True, 
     {'message': 'Promoção do prato atualizada com sucesso!'}),

    ("1234", True, "ATENDENTE", True, 
     {'error': 'Nível de permissão inválido!'}),

    ("9999", True, "GERENTE", False, 
     {'error': 'Prato não encontrado!'}),
])
@patch("app.db.collection")
def test_create_promocao(mock_db_collection, prato_id, promocao, permissao, prato_exists, expected):
    mock_doc = MagicMock()
    mock_doc.exists = prato_exists
    mock_db_collection.return_value.document.return_value.get.return_value = mock_doc

    result = create_promocao(prato_id, promocao, permissao)

    assert result == expected

    if prato_exists and permissao.upper().strip() == "GERENTE":
        mock_db_collection.return_value.document.return_value.update.assert_called_with({'promocao': promocao})
    else:
        mock_db_collection.return_value.document.return_value.update.assert_not_called()

if __name__ == "__main__":
    pytest.main()
