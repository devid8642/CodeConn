# Contribuindo
Segue abaixo um modelo de como contribuir com o projeto.

## Atualizando a master
Antes de criar uma branch e codar certifique-se de atualizar a sua master local. Então, estando na master você pode executar.

```
git pull origin master
```

## Criando um ramo
Crie um ramo que irá conter todas as suas alterações separadas da master, e depois troque para ele:

```
git branch <nome_da_branch>
```

```
git checkout <nome_da_branch>
```

Ou execute diretamente:

```
git checkout -b <nome_da_branch>
```

Agora siga codando e commitando normalmente.

## Concluindo seu trabalho
Agora, existem duas possibilidades, segue-se o que fazer em cada uma delas:

### Ainda não está terminado
Caso você tenha trabalhado em uma branch mas o que você queria fazer ainda não esteja pronto, simplesmente envie essa branch para o github e comunique os demais integrantes do projeto do que foi feito. Para enviar a branch para o github execute:

```
git push origin <nome_da_branch>:<nome_da_branch>
```

Se algum dos integrantes do projeto se sentir a vontade para dar continuidade ao trabalho ele deve executar:

```
git fetch origin
git checkout -b <nome_da_branch> origin/<nome_da_branch>
```

O primeiro comando baixa para o repo local tudo que foi adicionado de novo no GH, e o segundo cria uma nova branch local como sendo uma cópia da branch remotada do seu colega. Conclua o trabalho dele e faça o que vem a seguir ou se não conseguir concluir simplesmente repita o processo acima.

### Trabalho terminado
Nesse caso é hora de fazer o merge na master e enviar para o GH. Para isso primeiro troque para a master e atualize ela novamente:

```
git checkout master
git pull origin master
```

Após isso tente fazer o merge:

```
git merge <nome_da_branch>
```

O git deve ser capaz de resolver muitos conflitos sozinhos mas caso o merge não seja concluído (observe a saída do git para saber isso), ai é interessante entrar em contato com os integrantes do projeto para que isso seja feito com calma. Caso você observe que o conflito é simples, pode tentar resolver sozinho, apenas não apague código dos outros sem ter certeza do que você está fazendo.

Por fim delete a branch dê o push para o GH. O último comando so precisa ser executado caso a branch existe no GH também:

```
git branch -D <nome_da_branch>
git push
git push origin -d <nome_da_branch>
```

O segredo para minimizar os conflitos é o seguinte:

1. Lembre-se de sempre manter sua master atualizada.
2. Comunique-se com os outros integrantes da equipe sobre o que você está fazendo e em que ponto parou.