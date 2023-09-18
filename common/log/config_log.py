# -*- coding: utf-8 -*-

import logging.config
import logging.handlers
import os
from typing import Dict

import common.config as config

FORMAT = '{%(name)s} {%(levelname)s} {pid:%(process)d} {%(module)s.%(funcName)s:%(lineno)d} >>> %(message)s'


def get_rotating_file_handler_config(file_name: str) -> Dict:
    return {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'file',
        'filename': f"{config.log_path}/{file_name}",
        'maxBytes': 1024 << 17,
        'backupCount': 10,
        'encoding': 'utf-8'
    }


def get_rotating_file_handler(file_name: str):
    handler = logging.handlers.RotatingFileHandler(
        f"{config.log_path}/{file_name}",
        "a", maxBytes=1024 << 17,
        backupCount=10,
        encoding='utf-8')
    handler.setFormatter(logging.Formatter(f'%(asctime)s {FORMAT}'))
    return handler


def get_log_dict_config(level):
    return {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'console': {
                'format': FORMAT
            },
            'file': {
                'format': f'%(asctime)s {FORMAT}'
            },
        },
        'handlers': {
            'file': {
                'level': level,
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'file',
                'filename': f"{config.log_path}/root",
                'maxBytes': 1024 << 17,
                'backupCount': 10,
                'encoding': 'utf-8'
            },
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            }
        },
        'loggers': {
            'root': {
                'handlers': ['file'],
                'level': level,
            }
        }
    }


def create_file_logger(name: str):
    import os
    exists = os.path.exists(config.log_path)
    if not exists:
        os.mkdir(config.log_path)

    if not name.endswith(".log"):
        name = f'{name}.log'

    logger = logging.getLogger(name)
    logger.addHandler(get_rotating_file_handler(name))
    return logger


def initialize():
    console_log = os.environ.get("console_log", "ON").upper()
    log_level = os.environ.get("log_level", "INFO").upper()
    dict_conf = get_log_dict_config(log_level)
    os.makedirs(config.log_path, exist_ok=True)
    if console_log == "ON":
        dict_conf['loggers']["root"]['handlers'] = ['console']
    else:
        dict_conf['loggers']["root"]['handlers'] = ['file']

    logging.config.dictConfig(dict_conf)
