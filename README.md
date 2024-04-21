# Automatização para envio de mensagens/arquivos
Repositório dedicado a criação de uma automatização para enviar arquivos/mensagens utilizando a linguagem de programação python.

## Funcionalidades principais
- Permite enviar mensagens para uma lista de contatos
- Possibilita o envio de erquivos para uma lista de contatos

## Requisitos
O biblioteca utilizado no desenvolvimento deste projeto, utiliza comandos de teclado no padrão do Windows. Os testes foram realizados com a aplicação do WhatsApp Desktop sendo fixada na primeira posição da barra de tarefas do Windows.
Também é necessário realizar a instalação do SQL Server para coletar os dados dos contatos e a linguagem Python em sua maquina.

- Link para download do Python: [Python](https://www.python.org/downloads/)
- Link para download do SQL: [SQL Server Download](https://www.microsoft.com/pt-br/sql-server/sql-server-downloads)
- Link para download do SSMS: [SQL Server Management Studio (SSMS)](https://aka.ms/ssmsfullsetup)

## Instalação
Para realizar a instalação, siga estas etapas:
1. Clone o repositório do GitHub:
```bash
git clone https://github.com/Wiryco/automatizacaoMsg.git
```
2. Navegue até o diretório do projeto:
```bash
cd automatizacaoMsg
```
3. Instale as dependências usando pip:
```python
pip install -r requirements.txt
```
4. Instale o banco de dados SQL Server.
5. Navegue até o diretório onde está localizado o script modelo SQL:
```bash
cd sql
```
7. Execute o script dentro do SQL:
```sql
sqlmodel.sql
```
8. Execute o codigo principal python:
```python
python sendinfos.py
```

## Estrutura do projeto
```
projeto/
└── img/
    ├── botao_arquivo_desktop.png
    ├── botao_documento_desktop.png
    ├── botao_imagem_desktop.png
    ├── botao_imagem_web.png
    ├── botao_mensagem_desktop.png
    └── botao_pesquisa_desktop.png
└── sql/
    ├── sqlmodel.sql/
└── functions.py
└── scripts.py
└── sendinfos.py
└── .env
```

## Configuração do arquivo .env
O arquivo `.env` é usado para armazenar variáveis de ambiente que o seu projeto python precisa para funcionar corretamente.
Aqui está a estrutura básica do arquivo `.env` para este projeto:

```dotenv
serverName = ''
dataBase = ''
userName = ''
password = ''
driveConnection = ''
schema = ''
```

## Instalações pip manual
```
pip install SQLAlchemy
pip install pyautogui
pip install pynput
pip install python-dotenv
pip install pandas
pip install pyodbc
pip install --upgrade pillow
```

## Exemplos
Após a execução dos passos descritos anteriormente, é possível obter os dados dos clientes ao executar o seguinte comando no banco de dados:
```sql
SELECT C.*, A.ID_TIPO_ENVIO, B.DESCRICAO_TIPO_ENVIO, A.ID_MENSAGEM, A.CAMINHO_ARQUIVO, D.DESCRICAO_MENSAGEM
FROM automatizacao.CONTROLE_ENVIO_WPP A
JOIN automatizacao.TIPO_ENVIO_WPP B ON A.ID_TIPO_ENVIO = B.ID_TIPO_ENVIO
JOIN automatizacao.CONTATOS_WPP C ON A.ID_CONTATO = C.ID_CONTATO
JOIN automatizacao.MENSAGEM_WPP D ON A.ID_MENSAGEM = D.ID_MENSAGEM
WHERE C.ATIVO = 1
```
Ele vai trazer as seguintes informações:
```sql
ID_CONTATO	NOME	    TELEFONE	ATIVO	ID_TIPO_ENVIO	DESCRICAO_TIPO_ENVIO	ID_MENSAGEM	CAMINHO_ARQUIVO	                  DESCRICAO_MENSAGEM
2	        Nome Teste	99999999	1	    2	            DOCUMENTO	            0	        C:\testeSend\Teste RPA.txt	      NULL
2	        Nome Teste	99999999	1	    2	            DOCUMENTO	            0	        C:\testeSend\Teste RPA.docx	      NULL
2	        Nome Teste	99999999	1	    2	            DOCUMENTO	            0	        C:\testeSend\Teste RPA.pdf	      NULL
2	        Nome Teste	99999999	1	    3	            IMAGEM	                1	        C:\testeSend\harrypotter_2.jpeg	  Olá, tudo bem? Esse é um teste do robo que envia mensagem para os contatos do WhatsApp
```
Esta tabela será lida pela função `consultaDadosCliente`, disponibilizada no arquivo `scripts.py`, que retorna um dataframe contendo todas as informações dos contatos e os repositórios onde o Python vai coletar os arquivos que serão enviados.
O loop `for` percorre todas as posições do dataframe, coletando os dados dos clientes, os arquivos associados e enviando-os separadamente, um a um.
O loop `for` descrito é o seguinte:
```python
for contato in dba.select(query=query.consultaDadosCliente()).itertuples():
    contato_wpp = functions.contatoWpp(dadosContato=contato)

    contato_wpp.eventSelectUser()

    if contato.ID_TIPO_ENVIO == 1 and contato.DESCRICAO_MENSAGEM:
        contato_wpp.eventSendMsg()

    if (contato.ID_TIPO_ENVIO == 2 or contato.ID_TIPO_ENVIO == 3) and contato.CAMINHO_ARQUIVO:
        contato_wpp.eventClickFile()
        contato_wpp.eventSendFile()
```
