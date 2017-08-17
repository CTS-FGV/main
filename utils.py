import json
import requests
import copy
import collections
import psycopg2
import yaml
import datetime
import time
import hashlib


def convert_str_date(date, current_pattern, output_pattern):
    """
    Convert string date format from one pattern to another
    :param date: str:: date string
    :param current_pattern:  str:: current date pattern
    :param output_pattern:  str:: output date pattern
    :return: str:: output date
    """
    assert isinstance(date, str)
    assert isinstance(current_pattern, str)
    assert isinstance(output_pattern, str)

    dt = datetime.datetime.strptime(date, current_pattern).date()

    dt = dt.strftime(output_pattern)
    return dt


def daterange(start_date, end_date, convert=False, pattern=None):
    """
    Generate a range of dates between start_date and end_date

    :type convert: bool
    :param convert: bool

    if convert:
        :param start_date: str
        :param end_date: str
        :param pattern: str -> date pattern that was organized in string. eg: '%d-%m-%Y'
    else:
        :param start_date: datetime object
        :param end_date: datetime object

    :return: list -> list of datetime objects
    """
    if convert:
        start_date = datetime.datetime.strptime(start_date, pattern)
        end_date = datetime.datetime.strptime(end_date, pattern)

    day = start_date
    days_delta = (end_date - start_date).days
    for i in range(days_delta + 1):
        yield day
        day += datetime.timedelta(1)


def try_get_data(data_source, key, typ=None):
    try:
        value = data_source[key]
        if typ == 'int':
            value = int(value)
        elif typ == 'date':
            value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        elif typ == 'time':
            value = datetime.datetime.strptime(value, "%H:%M").time()

    except (KeyError, ValueError):
        value = None

    return value


def generate_hash(*args):
    """
    Generates a md5 hash value with a custom key, based in *args.
    :return:
    """
    key = bytes(' '.join(args), 'utf_8')
    hashh = hashlib.md5()
    hashh.update(key)
    return hashh.hexdigest()


def get_json(url):
    """
    Require a json url and convert in dict
    :param url: str | json url
    :return: dict | json
    """
    headers = {
        'accept': "application/json",
        'cache-control': "no-cache",
        'postman-token': "cce2e0c1-c598-842b-f15f-a1fe8b3e31e2"
    }

    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)


def slack_notify_dag_error(context):
    """
    Slack notification when a DAG fail.
    This function should be used in on_failure_callback parameter of BashOperator.
    """

    dag_id = str(context['dag'])
    dag_id = dag_id[6:-1]

    task_id = str(context['task'])
    task_id = task_id[21:-1]

    dia = context['ds']

    hora = context['ts'][11:]

    link = "http://172.16.4.227:8080/admin/airflow/log?task_id={}&dag_id={}&execution_date={}".format(
        task_id, dag_id, context['ts'])

    mensagem = "DAG_ID: {} \n TASK_ID: {} \n DATA: {} \n HORA: {}".format(dag_id, task_id, dia, hora)

    data = {"attachments": [
                {"fallback": "Deu Erro! Fale com @alifersales",
                 "title": "Erro ao executar DAG",
                 "title_link": link,
                 "fields": [
                     {"value": mensagem}
                     ],
                 "color": "#ff0000"}]}

    data = str(data)

    headers = {'Content-type': 'application/json'}

    requests.post('https://hooks.slack.com/services/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',
                  headers=headers, data=data)


def _strip_all(dic):
    """
    Strip values deleting spaces, \t and \n chars.
    :param dic:
    :return:
    """
    for k, v in dic.items():

        if len(v) == 0:
            dic[k] = 'NULL'
        if isinstance(v, str):
            v = v.strip().replace('\t', '').replace('\n', '').encode('utf-8', 'ignore')
            dic[k] = v

    return dic


def _get_values(full_dic, all_keys, skeleton):
    """
    Insert values from the xml to the skeleton dict using the paths stored in a skeleton tuple
    :param full_dic: dict:: Xml dict
    :param all_keys: List of Tuples :: Path to all variables
    :param skeleton: dict :: SQL skeleton
    :return:
    """
    for key_list in all_keys:

        # try to see if tree exists on xml
        tree_dic = copy.copy(full_dic)

        for l in key_list:
            try:
                # caso que value do dict é lista
                if isinstance(tree_dic, list):
                    tree_dic = tree_dic[0]
                tree_dic = tree_dic[l]
            except KeyError:
                pass

        if isinstance(tree_dic, list):  # caso que value do dict é lista
            tree_dic = tree_dic[0]

        # if it exists, add values to dic
        for k, v in tree_dic.items():
            if isinstance(v, dict) or isinstance(v, list) or len(key_list) == 0:
                continue

            column = key_list[-1] + '_' + k
            if column in skeleton.keys():
                skeleton[column] = v

    return skeleton


def connect_psycopg2():
    """
     Create psycopg2 connection with PostgreSQL database
     :return: psycopg2 connection
     """
    server = yaml.load(open('config.yaml', 'r'))

    server = server['servers'][229]

    host = server['host']
    database = server['database']
    user = server['user']
    password = server['password']

    conn = psycopg2.connect(
        host=host, port=5432, database=database,
        user=user, password=password)
    return conn


def connect_sqlalchemy():
    """
    Create SQLalchemy connection with PostgreSQL database
    :return: SQLalchemy connection
    """

    server = yaml.load(open('config.yaml', 'r'))

    server = server['servers'][229]

    host = server['host']
    database = server['database']
    user = server['user']
    password = server['password']

    from sqlalchemy import create_engine
    url = 'postgresql://{}:{}@{}/{}'
    url = url.format(user, password, host, database)
    return create_engine(url)


if __name__ == '__main__':
    pass
