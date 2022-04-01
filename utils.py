from config.config import config

def symbol(tick1, tick2=config["ref_token"]):
    return f'{tick1}/{tick2}'

def drop_message(dic):
    s = ""
    for val, key in dic.items():
        s.append(f'{key} dropped {val}% \n')
    return s
