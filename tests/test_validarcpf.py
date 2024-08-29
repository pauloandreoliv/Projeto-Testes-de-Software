import pytest
from app import validar_cpf

def test_validar_cpf_valido():
    cpf = "12345678901"
    assert validar_cpf(cpf) == True

def test_validar_cpf_invalido_caracteres_nao_numericos():
    cpf = "1234567890a"
    assert validar_cpf(cpf) == False

def test_validar_cpf_invalido_menos_de_11_digitos():
    cpf = "1234567890"
    assert validar_cpf(cpf) == False

def test_validar_cpf_invalido_mais_de_11_digitos():
    cpf = "123456789012"
    assert validar_cpf(cpf) == False

def test_validar_cpf_vazio():
    cpf = ""
    assert validar_cpf(cpf) == False

def test_validar_cpf_caracteres_especiais():
    cpf = "123.456.789-01"
    assert validar_cpf(cpf) == False

if __name__ == "__main__":
    pytest.main()