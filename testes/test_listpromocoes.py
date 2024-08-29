import pytest
from unittest.mock import patch, MagicMock
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase
from app import list_promocoes, db

def test_list_promocoes_bd():
    docs = db.collection('prato').stream()
    for doc in docs:
        doc.reference.delete()

    prato_a = db.collection('prato').add({'nome': 'Prato A', 'valor': 25.50, 'promocao': True})
    prato_b = db.collection('prato').add({'nome': 'Prato B', 'valor': 30.00, 'promocao': True})
    resultado = list_promocoes()

    resultado_sorted = sorted(resultado, key=lambda x: x['nome'])
    assert resultado_sorted == [
        {'id': prato_a[1].id, 'nome': 'Prato A', 'valor': 25.50, 'promocao': True},
        {'id': prato_b[1].id, 'nome': 'Prato B', 'valor': 30.00, 'promocao': True}
    ]
    docs = db.collection('prato').stream()
    for doc in docs:
        doc.reference.delete()
    resultado = list_promocoes()
    assert resultado == {'error': 'Nenhum prato em promoção encontrado!'}

if __name__ == "__main__":
    import pytest
    pytest.main()
