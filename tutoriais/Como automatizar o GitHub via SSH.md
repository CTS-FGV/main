## How to Automate Push to GitHub via SSH and Airflow

How to create repo that gives automatic push on GitHub for Ubuntu

1. Create a repository with the following [nomenclature](https://github.com/CTS-FGV/geral)

2. If there is already a page that you will put in Git, check if the server settings are not exposed in ALL FILES. The server settings must be in a file of the type yaml or cfg. *DO NOT FORGET!*.

3. Create a file in the root of the folder named `.gitiginore` to skip the configuration and data files. The content is:

```
# Server Config
* .yaml
* .cfg

Date
* .csv
* .xlsx
```

4. Enter this folder in the terminal and initialize a git pointing to the repository via ssh.

```
git init
git remote add origin git@github.com: [user_name / group_name] / [repository_name] .git
git remote set-url origin git@github.com: [user_name / group_name] / [repository_name] .git
```

Example:
`git remote set-url origin git@github.com: CTS-FGV / congress-analysis.git`

Now we have to connect to Git via SSH.

5. Check if there is a SSH key on the machine with:
`ls -al ~ / .ssh`. If there are already the files named `id_rsa.pub` and` id_rsa` then someone has already made the SSH connection.

If there is a connection, go to step 10.

6. Create a public and private ssh key for your server

`ssh-keygen -t rsa -b 4096 -C" [user @ mail] `


7. Get ssh agent running with,

`eval '$ (ssh-agent -s)` 

8. Add the private key to `id_rsa`:

`ssh-add ~ / .ssh / id_rsa`

9. Link your github account with ssh via public key. First copy the key using,your favorite text editor, (hint: use vim). Then open your GitHub settings, go to _SSH and GPG keys_ and enter a new SSH key.

`Vim ~ / .ssh / id_rsa.pub`

10. Now just do the default git add, commit, push that everything must happen automatically.

11. Now we have to configure Airflow. Go to server 227 and enter in the dag responsible for the auto_git at `/ home / Admin / airflow / dags / auto_git.py`. Add in the file a new task in the DAG with the same name of the repository. Point it to the right `path` and check if it is the same as the bash file of the file in question. Do not forget to place the process at the end of the airflow chain. A new process should look like this:

```
path = [path_to_folder]
[repo_name] = BashOperator(
                    task_id='[repo_name]',
                    bash_command= BASH_SCRIPT,
                    params={'to_server': [to_227 or to_228], # choose the server that your repo is stored
                            'path': path},
                    on_failure_callback=utils.slack_notify_dag_error,
                    dag=dag)
```

12. Test the task using `airflow test auto_git [repo_name] 2015-06-01`. If it worked, success!
