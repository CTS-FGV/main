## Creating Repositories

#### Check if it is in one of the following categories. Otherwise, get in contact with @JoaoCarabetta.
- to backup project code
- to backup infrastructure code
- a branch of a project that has community potential

#### Now, give it a name according to those rules:

- Add the root of your desktop. The name to be chosen is _ [project_name] _ [repository_type].
```
Example: congresso_analise, corrupcao_captura
```
- If you think one of the subprojects is very important and can be a repository by itself, add with the name:
[Project_name] __proj__ [repository_type].
```
Example: congresso_proj_redes
```

- If it is an infrastructure-related repository use infra_[explicative_name]
```
Example: infra_airflow
```
#### With the repository created, identify which server is most fitted to your project. The servers have the following functions:

- 226: web-related uses, websites, etc.
- 227: scrapers and capture scripts
- 228: analysis scripts and jupyter envi
- 229: databases

#### Now, you have to create a folder on the choosen server with the same name. The paths for each server are:

- 226: /
- 227: /
- 228: home/Admin/cts/
- 229: /

#### Copy all the code that you already had somewhere else to this folder and proceed to the [next tutorial](https://github.com/CTS-FGV/geral/blob/master/tutoriais/Como%20automatizar%20o%20GitHub%20via%20SSH.md) on how to sync with airflow.
