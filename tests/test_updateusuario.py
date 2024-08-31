import pytest
from unittest.mock import patch, MagicMock
from app import update_usuario
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase


@pytest.mark.parametrize("cpf, update_data, mock_validar_cpf_result, mock_usuario_docs, expected", [
    ("12345678909", {'email': 'novoemail@email.com', 'telefone': '9999999999'}, True, [MagicMock(id='usuario_id')], {'message': 'Usuário atualizado com sucesso!'}),
    
    ("00000000000", {'email': 'novoemail@email.com'}, False, None, {'error': 'CPF inválido!'}),
    
    ("11111111111", {'email': 'novoemail@email.com'}, True, [], {'error': 'Usuário não encontrado!'}),
])
@patch('app.db.collection')
@patch('app.validar_cpf')
def test_update_usuario(mock_validar_cpf, mock_db_collection, cpf, update_data, mock_validar_cpf_result, mock_usuario_docs, expected):
    mock_validar_cpf.return_value = mock_validar_cpf_result
    
    mock_collection = mock_db_collection.return_value
    mock_collection.where.return_value.stream.return_value = mock_usuario_docs
    
    if mock_usuario_docs:
        mock_doc = mock_collection.document.return_value
        mock_doc.update = MagicMock()
    
    resultado = update_usuario(cpf, update_data)
    assert resultado == expected
    
    if expected.get('message') == 'Usuário atualizado com sucesso!':
        mock_collection.document.assert_called_once_with(mock_usuario_docs[0].id)
        mock_doc.update.assert_called_once_with(update_data)

@patch('app.db.collection')
def test_update_usuario_excecao(mock_db_collection):
    mock_db_collection.side_effect = Exception("Erro inesperado!")
    resultado = update_usuario("12345678909", {'email': 'novoemail@email.com'})
    assert resultado == {'error': 'Erro Inesperado'}

if __name__ == "__main__":
    pytest.main()
