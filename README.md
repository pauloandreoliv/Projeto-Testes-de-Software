# Plano de Testes - Sistema de Pedidos de Restaurante

**Versão 1.1**

## Iteração 1

### Casos de Uso

| Identificador do Caso de Uso | Nome do Caso de Uso                |
|------------------------------|-------------------------------------|
| CDU1                         | Registro de Clientes               |
| CDU3                         | Criação de Pedido                  |
| CDU5                         | Autenticação de Usuário (Login)     |
| CDU16                        | Login de Funcionário               |
| CDU18                        | Criar Prato                        |
| CDU13                        | Visualizar Todos os Pratos         |

## Iteração 2

### Casos de Uso

| Identificador do Caso de Uso | Nome do Caso de Uso                |
|------------------------------|-------------------------------------|
| CDU4                         | Atualização de Informações de Clientes |
| CDU6                         | Listagem de Pedidos                |
| CDU7                         | Consultar Pedido por CPF           |
| CDU10                        | Gerenciar Promoção                 |
| CDU12                        | Visualizar Pratos em Promoção      |
| CDU14                        | Excluir Prato                      |
| CDU17                        | Cadastrar Funcionário              |

## Iteração 3

### Casos de Uso

| Identificador do Caso de Uso | Nome do Caso de Uso                |
|------------------------------|-------------------------------------|
| CDU2                         | Notificação de Confirmação de Pedido por E-mail |
| CDU8                         | Visualizar Minhas Informações      |
| CDU9                         | Consultar Promoção                 |
| CDU11                        | Consultar Prato                    |
| CDU15                        | Consultar Informações de Funcionário |
| CDU19                        | Avaliar Pedido                     |
| CDU20                        | Cálculo da Média de Avaliações     |

## Tipos de Teste

### Iteração 1

- **Objetivo**: Durante esta iteração, serão realizados testes dos requisitos básicos para o funcionamento do sistema, visando verificar a solidez do sistema.
- **Técnica**: Automática
- **Estágio do Teste**: Unidade
- **Abordagem do Teste**: Caixa Branca
- **Responsável(is)**: Programadores

### Iteração 2

- **Objetivo**: Ao longo desta iteração, serão realizados testes dos requisitos complementares ao funcionamento do sistema, que permitem uma melhor usabilidade e possuem alta relevância, visando verificar a adequação de seu funcionamento.
- **Técnica**: Automática
- **Estágio do Teste**: Unidade
- **Abordagem do Teste**: Caixa Branca
- **Responsável(is)**: Programadores

### Iteração 3

- **Objetivo**: Nesta iteração, serão testados requisitos que não são essenciais ao funcionamento do sistema, mas complementam a nível de experiência dos usuários e facilitam a execução de atividades.
- **Técnica**: Automática
- **Estágio do Teste**: Unidade
- **Abordagem do Teste**: Caixa Branca
- **Responsável(is)**: Programadores

## Formato do Plano de Testes

**Exemplo**:
4. Consultar Prato
Teste 1: ID do prato válido
Entrada 1: prato_id = "1234"
Saída 1: Dados do prato em formato de dicionário

Teste 2: ID do prato inválido ou não informado
Entrada 2: prato_id = ""
Saída 2: Mensagem de erro: {"error": "ID do prato deve ser informado!"}

## Ambiente de Teste – Software & Hardware
1. Hardware: Computador Desktop
- **Processador**: Intel Core i5 (ou equivalente)
- **Memória RAM**: 4 GB
- **Armazenamento**: SSD de 256 GB

2. Software:
- **Sistema Operacional**: Windows 11
- **IDE/Editor de Código**: Visual Studio Code (VSCode) versão 1.83.0 (ou versão mais recente)
- **Banco de dados**: Firebase Firestore (NoSQL Documento)
- **Versão do Python**: Python 3.11.4
- **Dependências**:
pytest (para execução de testes automáticos)
unittest.mock (geração de mocks)
pytest-cov (Métrica de cobertura)
re
firebase_admin
smtplib
datetime
email.mime.multipart
email.mime.text

3. Configurações adicionais:
Necessária a geração de um novo arquivo key.json no caso de exposição da chave privada. Também é necessário estar conectado a uma rede de internet com conexão estável.

## Ferramentas de Teste
- **Biblioteca de testes automatizados**: Pytest
- **Biblioteca de mocks**: unittest.mock
- **Biblioteca de métrica de cobertura**: pytest-cov
- **IDE**: Visual Studio Code (VSCode)

## Observações
1. Para executar os testes basta executar o arquivo **run_tests.py**;
2. Em caso de verificação das métricas, pode ser necessário mover os arquivos da pasta **tests** para o diretório principal, junto ao **app.py**;
3. A chave privada **key.json** é desativada ao ser exposta no GitHub, desse modo foi necessário disponibilizá-la externamente no Google Drive [Clique aqui para acessar a chave privada](https://drive.google.com/file/d/1pTjyhBp8DAgrq_RJ_F0CGKDBQslKpfpN/view?usp=sharing). Ao baixá-la é necessário apenas inseri-la no diretório principal,  junto ao **app.py**.