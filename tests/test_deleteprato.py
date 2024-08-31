import pytest
from unittest.mock import patch, MagicMock
from app import delete_prato
import warnings
warnings.filterwarnings('ignore')  # Ignorar warnings do Firebase

@pytest.mark.parametrize("prato_id, permissao, mock_prato_exists, expected", [
    ("123", "GERENTE", True, {'message': 'Prato excluído com sucesso!'}),
    ("123", "ATENDENTE", True, {'error': 'Nível de permissão inválido!'}),
    ("", "GERENTE", True, {'error': 'ID do prato deve ser informado!'}),
    ("999", "GERENTE", False, {'error': 'Prato não encontrado!'}),
])
@patch('app.db.collection')
def test_delete_prato(mock_db_collection, prato_id, permissao, mock_prato_exists, expected):
    mock_document = MagicMock()
    mock_document.get.return_value.exists = mock_prato_exists
    mock_db_collection.return_value.document.return_value = mock_document
    resultado = delete_prato(prato_id, permissao)
    assert resultado == expected

    if permissao.upper().strip() == 'GERENTE' and prato_id and mock_prato_exists:
        assert mock_db_collection.call_count == 2

        mock_db_collection.assert_any_call('prato')
        mock_db_collection.return_value.document.assert_any_call(prato_id)
        mock_db_collection.return_value.document.return_value.get.assert_called_once()

        mock_db_collection.assert_any_call('prato')
        mock_db_collection.return_value.document.return_value.delete.assert_called_once()

@pytest.mark.parametrize("prato_id, permissao, expected", [
    ("123", "GERENTE", {'error': 'Erro Inesperado'}),
])
@patch('app.db.collection')
def test_delete_prato_excecao(mock_db_collection, prato_id, permissao, expected):
    mock_db_collection.return_value.document.return_value.delete.side_effect = Exception("Unexpected error")
    
    resultado = delete_prato(prato_id, permissao)
    
    assert resultado == expected

if __name__ == "__main__":
    pytest.main()