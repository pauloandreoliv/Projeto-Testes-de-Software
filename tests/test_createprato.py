import pytest
from unittest.mock import patch, MagicMock
from app import create_prato
import warnings 
warnings.filterwarnings('ignore')  # Ignorar warning do firebase

@pytest.mark.parametrize("nome, url_img, valor, permissao, side_effect, expected", [
    ("Prato A", "img_url", 25.50, "GERENTE", 
     None, {'message': 'Cadastro realizado com sucesso!', 'id': 'doc_id'}),

    ("Prato A", "img_url", 25.50, "ATENDENTE", 
     None, {'error': 'Nível de permissão inválido!'}),

    ("Prato A", "", 25.50, "GERENTE", 
     None, {'error': 'Todos os campos devem ser preenchidos!'}),

    ("Prato A", "img_url", -10, "GERENTE", 
     None, {'error': 'Valor deve ser maior que zero!'}),

    ("Prato A", "img_url", 25.50, "GERENTE", 
     Exception("Erro Inesperado"), {'error': 'Erro Inesperado'}),
])
@patch("app.db.collection")
def test_create_prato(mock_db_collection, nome, url_img, valor, permissao, side_effect, expected):
    mock_add = MagicMock()
    
    if side_effect:
        mock_db_collection.return_value.add.side_effect = side_effect
    else:
        mock_db_collection.return_value.add.return_value = (None, mock_add)
        mock_add.id = "doc_id"

    result = create_prato(nome, url_img, valor, permissao)
    
    if 'id' in result:
        expected['id'] = "doc_id"

    assert result == expected

if __name__ == "__main__":
    pytest.main()
