import pytest
from unittest.mock import patch, MagicMock
from app import create_promocao
import warnings 
warnings.filterwarnings('ignore')  # Ignorar warning do firebase

@pytest.mark.parametrize("prato_id, promocao, permissao, prato_exists, side_effect, expected", [
    ("1234", True, "GERENTE", True, None, 
     {'message': 'Promoção do prato atualizada com sucesso!'}),

    (None, True, "GERENTE", False, None, 
     {'error': 'ID do prato deve ser informado!'}),

    ("1234", None, "GERENTE", False, None, 
     {'error': 'O valor de promoção deve ser True ou False!'}),

    ("1234", True, "ATENDENTE", True, None, 
     {'error': 'Nível de permissão inválido!'}),

    ("9999", True, "GERENTE", False, None, 
     {'error': 'Prato não encontrado!'}),

    ("1234", True, "GERENTE", True, Exception("Erro Inesperado"), 
     {'error': 'Erro Inesperado'}),
])
@patch("app.db.collection")
def test_create_promocao(mock_db_collection, prato_id, promocao, permissao, prato_exists, side_effect, expected):
    mock_doc = MagicMock()
    mock_doc.exists = prato_exists

    if side_effect:
        mock_db_collection.return_value.document.return_value.get.side_effect = side_effect
    else:
        mock_db_collection.return_value.document.return_value.get.return_value = mock_doc

    result = create_promocao(prato_id, promocao, permissao)

    assert result == expected

    if not side_effect and prato_exists and permissao.upper().strip() == "GERENTE":
        mock_db_collection.return_value.document.return_value.update.assert_called_with({'promocao': promocao})
    else:
        mock_db_collection.return_value.document.return_value.update.assert_not_called()

if __name__ == "__main__":
    pytest.main()
