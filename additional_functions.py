import json


def write_info_about_game(*info):
    """Func to writing information in log file. """
    with open('server_info.txt', 'a') as f:
        info = json.dumps(info)
        f.write(info + '\n')


def info_in_json(info):
    """Func to create encoding json. """
    info = json.dumps(info)
    return info.encode('utf-8')


def info_from_json(info):
    """Func to decode information and to convert json in python. """
    return json.loads(info.decode('utf-8'))
