import pytest
from unittest.mock import patch, MagicMock
from app import calcular_media_avaliacoes
import warnings 
warnings.filterwarnings('ignore')  # Ignorar warning do firebase


@pytest.mark.parametrize("permissao, mock_avaliacoes, side_effect, expected", [
    ("GERENTE", [MagicMock(to_dict=lambda: {'nota': 8}), MagicMock(to_dict=lambda: {'nota': 9}), MagicMock(to_dict=lambda: {'nota': 7})], 
     None,
     {'message': 8.0}),
     
    ("COZINHEIRO", None, 
     None,
     {'error': 'Nível de permissão inválido!'}),

    ("GERENTE", [], 
     None,
     {'error': 'Nenhuma avaliação encontrada!'}),

    ("GERENTE", [MagicMock(to_dict=lambda: {'nota': 8}), MagicMock(to_dict=lambda: {'nota': 9}), MagicMock(to_dict=lambda: {'nota': 7})], 
     Exception("Erro Inesperado"), 
     {'error': 'Erro Inesperado'}),
])
@patch('app.db.collection')
def test_calcular_media_avaliacoes(mock_db_collection, permissao, mock_avaliacoes, side_effect, expected):
    if mock_avaliacoes is not None:
        mock_collection = mock_db_collection.return_value
        mock_collection.stream.return_value = mock_avaliacoes
        
        if side_effect:
            mock_collection.stream.side_effect = side_effect 
    resultado = calcular_media_avaliacoes(permissao)
    assert resultado == expected
    
    if permissao.upper().strip() in ['ATENDENTE', 'GERENTE']:
        mock_db_collection.assert_called_once_with('avaliacao')
        if permissao.upper().strip() == 'GERENTE' and not side_effect:
            mock_db_collection.return_value.stream.assert_called_once()

if __name__ == "__main__":
    pytest.main()
