# TRABALHO FINAL DE REDES

## Requisitos

- Python: >= 3.7

## Como instalar

Execute o comando `pip install -r ./requirements.txt` para instalar as dependências do projeto

## Como usar

### Tracker

- Veja o IP da máquina que irá hospedar o tracker
- Altere a linha 39 com IP do arquivo `server.py`
- Execute o comando `python ./server.py` para iniciar o Tracker

### Cliente

- Com o IP do Tracker altere a linha 26 do arquivo `client.py`
- Crie uma pasta no diretório raiz contendo os arquivos do cliente
- Execute o comando `python ./client.py nome_da_pasta nome_do_cliente`
- O cliente recebe dois parâmetros para funcionar: a pasta com os arquivos e o nome dele
- O nome do cliente é utilizado para caso o cliente entre de outro IP ainda possa manter a mesma conexão
- OBS: Caso necessário altere a linha 24 informando diretamente o IP da máquina

## Autores

- Eduardo Henrique
- Vinicius Coelho
