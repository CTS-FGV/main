## Como automatizar o push para o GitHub via SSH e Airflow

Como criar repo que dá push automático no GitHub para Ubuntu

1. Crie um repositório com a seguinte nomenclatura:

*[nome_do_projeto]_[tipo_do_repositório]*

Exemplo: congresso_analise, corrupcao_captura

2. Se já existe uma página que você vai colocar no Git, cheque em todos os arquivos se as configurações do servidor não estão expostas. *NÃO ESQUEÇA!*.

3. Crie um arquivo na raiz da pasta chamado `.gitiginore` para ignorar os arquivos de configuração e de dados. O conteúdo é:

```
# Server Config
*.yaml
*.cfg

Data
*.csv
*.xlsx
```

4. Entre nessa pasta no terminal e inicialize um git apontando para o repositório via ssh

```
git init
git remote set-url origin git@github.com:[nome_do_usuário/nome_do_grupo]/[nome_do repositório].git
```
Exemplo:
`git remote set-url origin git@github.com:CTS-FGV/congresso-analise.git`

Agora temos se conectar ao Git via SSH.

5. Cheque se já não existe uma chave SSH na máquina com:
`ls -al ~/.ssh`. Se já existir os arquivos chamados `id_rsa.pub` e `id_rsa` então alguém já fez a conexão de SSH.

Caso exista conexão vá para passo 10.

6. Crie uma chave pública e privada ssh para seu servidor 

`ssh-keygen -t rsa -b 4096 -C "[user@mail]`


7. Comece o agente de ssh com

`eval "$(ssh-agent -s)"`

8. Adicione a private key ao `id_rsa`:

`ssh-add ~/.ssh/id_rsa`

9. Faça o link da sua conta github com o ssh via chave pública. Primeiro copie a chave usando, ou copie direto do seu editor de texto favorito, (dica:use vim)

```
sudo apt-get install xclip
xclip -sel clip < ~/.ssh/id_rsa.pub
```

ou

`vim ~/.ssh/id_rsa.pub`

10. Agora é só fazer o git add, commit, push padrão que tudo deve ocorrer automaticamente. 

11. Vá na raiz da pasta que é o repositório e adicione o arquivo 'auto_git.sh' com o seguinte conteúdo:

```
#!/bin/bash  
git add .
git commit -m "auto_commit"
git push
```

e rode no terminal `chmod 755 auto_git.sh`

12. Agora temos que configurar o Airflow. Vá no servidor 227 e entre na dag responsável pelos auto pushs no airflow `/home/Admin/airflow/dags/auto_git.py` e no ariquivo uma nova etapa na DAG com o mesmo nome do repositório. Atente-se ao `path` e cheque se é o mesmo do bash file do arquivo em questão. Não esqueça de colocar o processo no final da cadeia de airflow. Um novo processo deve ficar assim:

```
path = '[path_to_auto_git]'
[nome_do_repo] = BashOperator(
                    task_id='[nome_do_repo]',
                    bash_command= path + file_name,
                    dag=dag)
```

13. Teste a task usando `airflow test auto_git [nome_da_task] 2015-06-01`. Se funcionou, sucesso! 



