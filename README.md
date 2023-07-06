# Code Connect
O Code Connect foi criado por alunos e estudantes de programação, ele tem o propósito de estimular e incentivar outros como nós a por em prática o que aprendemos no dia a dia na área de tecnologia e sair do ócio. Deixar de ser o "programador" que apenas lê artigos ou copia códigos de vídeos e não cria nada próprio.

### Como funciona

O site funciona como um portifólio geral para os alunos de Ciência da Computação e áreas afins da Estácio. Os alunos cadastrados e verificados no site terão um prazo em torno de duas semanas ou mais para criarem seus próprios projetos e postarem na plataforma. Lembrando que o projeto não precisa ser algo enorme, pode ser algo simples e não precisa estar completo, o importante é se desafiar a algo novo, por em prática seus conhecimentos e aprender com os próprios erros!

## Setup do projeto
Após baixar o código do projeto localmente, crie um ambiente virtual com o python:

```
python -m venv venv
```

Ativo-o em um ambiente Linux com:

```
source venv/bin/activate
```

Em um ambiente Windows:

```
Scripts/activate.bat
```

### Instalando as dependências
Instalando via pip:

```
pip install -r requirements.txt
```

Instalando via poetry:

```
poetry install
```

### Variáveis de Ambiente
Crie na raiz do projeto um arquivo de nome .env com as mesmas variáveis listadas no arquivo env.example. As variáveis referentes ao servidor de email e ao banco de dados só devem ser setadas caso você deseje simular o ambiente de produção. Para isso considere utilizar um servidor SMTP como o Gmail e um servidor de banco de dados PostgreSQL devidamente configurados.

### Criando o schema do banco de dados
Para isso execute:

```
python manage.py migrate
```

### Rodando a aplicação
Para isso execute

```
python manage.py runserver
```

### Rodando os tests
Para rodar todos os testes da aplicação execute:

```
pytest
```

## Contribuindo
Segue o arquivo para os participantes do projeto com o guia de contribuição: [contribuindo](contrib.md)

## Detalhes do projeto
Toda a organização do backend do projeto está aqui: [documentação do projeto](https://hilarious-wound-b4c.notion.site/CodeConnect-fbc072db38b04db9b38bc5fa9f29b3b2?pvs=4).
