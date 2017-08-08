# Introdução
Infelizmente, o processo de remoção de uma DAG não é tão simples quanto a sua criação. Apenas remover o arquivo (_ou as linhas de código_) da pasta dags não faz com que ela "suma" da web GUI.

Este tutorial ensinará porquê isso acontece e como contornar isso.

Se você não estiver interessado no passo a passo do processo, encontre no fim deste arquivo uma função que automatiza a remoção da dag.

# Por que não basta remover o arquivo da DAG?
Quando o Airflow reconhece uma nova DAG através de um arquivo na pasta `dags/`, ele se encarrega de inseri-la no seu banco de dados. É considerado que o 

continue...
