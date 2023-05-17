# Projeto X
Gerenciador de projetos para uma organização independente de alunos da Estácio.

## Setup do projeto
Foi feito o setup do projeto em uma máquina com o python versão 3.10.11 e poetry 1.4.2, recomendo está versão em específico para rodar o projeto. Além disso, seguindo as boas práticas de projetos python, crie antes de tudo um ambiente virtual para instalar tudo, na linha de comando:

<code>
    python -m venv venv
</code>

Este comando criará um ambiente virtual de nome venv no diretório atual. Ativo-o em um ambiente Linux com:

<code>
    source venv/bin/activate
</code>

Em um ambiente Windows:

<code>
Scripts/activate.bat
</code>

### Instalando as dependências
Instalando via pip:

<code>
pip install -r requirements.txt
</code>

Instalando via poetry:

<code>
poetry install
</code>

### Criando o arquivo .env
Crie na raiz do projeto um arquivo de nome .env com as mesmas variáveis listadas no arquivo env.example. O valor da variável SECRET_KEY fica a seu gosto, porém é importante que você adote a variável PRODUCTION como False a não ser que você queira emular em sua máquina o ambite de produção, o que eu não recomendo pois depende de mais dependências que talvez seu computador não tenha.

### Criando o schema do banco de dados
Para isso execute:

<code>
python manage.py migrate
</code>

### Rodando a aplicação
Para isso execute

<code>
python manage.py runserver
</code>

### Rodando os tests
Para rodar todos os testes da aplicação execute:

<code>
pytest
</code>

## Dependências de produção
--- VOU ESCREVER DPS ---

## Detalhes do projeto
Toda a organização do backend do projeto está aqui: [backend do projeto](https://hilarious-wound-b4c.notion.site/Gerenciador-de-projetos-fbc072db38b04db9b38bc5fa9f29b3b2)