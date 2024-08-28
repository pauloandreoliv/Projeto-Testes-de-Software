import pytest
from unittest.mock import patch, MagicMock
from app import create_prato

@pytest.mark.parametrize("nome, url_img, valor, permissao, expected", [
    ("Prato A", "img_url", 25.50, "GERENTE", 
     {'message': 'Cadastro realizado com sucesso!', 'id': 'doc_id'}),

    ("Prato A", "img_url", 25.50, "ATENDENTE", 
     {'error': 'Nível de permissão inválido!'}),

    ("Prato A", "img_url", -10, "GERENTE", 
     {'error': 'Valor deve ser maior que zero!'}),
])
@patch("app.db.collection")
def test_create_prato(mock_db_collection, nome, url_img, valor, permissao, expected):
    mock_add = MagicMock()
    mock_db_collection.return_value.add.return_value = (None, mock_add)
    mock_add.id = "doc_id"

    result = create_prato(nome, url_img, valor, permissao)
    if 'id' in result:
        expected['id'] = "doc_id"

    assert result == expected

if __name__ == "__main__":
    pytest.main()