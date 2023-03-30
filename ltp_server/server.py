# -*- coding: utf-8 -*-
import os
from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ltp import LTP
from ltp import StnSplit
from fire import Fire
import yaml
import util

CONFIG_PATH = "config.yml"

with open(os.path.join(os.path.dirname(__file__), CONFIG_PATH)) as file:
    config = yaml.safe_load(file.read())


class Item(BaseModel):
    texts: List[str]


class LoginInfo(BaseModel):
    username: str
    password: str


class Words(BaseModel):
    words: List[str]
    max_window: int = 4


class Server:
    def __init__(self, dict_path: str = None, max_window: int = 4):
        self._app = FastAPI()
        self._ltp = LTP()
        self._stn_split = StnSplit()
        self
        if dict_path:
            self._ltp.init_dict(path=dict_path, max_window=max_window)
        self._init_sys()
        self._init_ltp()

    def _init_ltp(self):
        @self._app.post(config["route_path"]['ltp']["sent_split"])
        def stn_split(item: Item):  # 分句
            ret = {
                'texts': item.texts,
                'stn_split': [],
            }
            try:
                res = self._ltp._stn_split.split(item.texts)
                ret['stn_split'] = res
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]['ltp']["add_words"])
        def add_words(words: Words):  # 增加自定义词语
            ret = {
                'status': 0
            }
            try:
                self._ltp.add_words(words=words.words,
                                    max_window=words.max_window)
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]['ltp']["cws"])
        def cws(item: Item):  # 分词
            ret = {
                'texts': item.texts,
            }
            try:
                cws = self._ltp.pipeline(
                    item.texts, tasks=['cws']).to_tuple()
                ret['cws'] = cws
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

        @self._app.post(config["route_path"]['ltp']["pos"])
        def pos(item: Item):  # 词性标注
            ret = {
                'texts': item.texts,
            }
            try:
                cws, pos = self._ltp.pipeline(
                    item.texts, tasks=["cws", "pos"]).to_tuple()
                ret['pos'] = pos
                ret['cws'] = cws
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

        @self._app.post(config["route_path"]['ltp']["ner"])
        def ner(item: Item):  # 命名实体识别
            ret = {
                'texts': item.texts,
            }
            try:
                cws, ner = self._ltp.pipeline(
                    item.texts, tasks=["cws", "ner"]).to_tuple()
                ret['ner'] = ner
                ret['cws'] = cws
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

        @self._app.post(config["route_path"]['ltp']["srl"])
        def srl(item: Item):  # 语义角色标注
            ret = {
                'texts': item.texts,
            }
            try:
                cws, srl = self._ltp.pipeline(
                    item.texts, tasks=["cws", "srl"]).to_tuple()
                ret['srl'] = srl
                ret['cws'] = cws
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

        @self._app.post(config["route_path"]['ltp']["dep"])
        def dep(item: Item):  # 依存句法分析
            ret = {
                'texts': item.texts,
            }
            try:
                cws, dep = self._ltp.pipeline(
                    item.texts, tasks=["cws", "dep"]).to_tuple()
                ret['dep'] = dep
                ret['cws'] = cws
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

        @self._app.post(config["route_path"]['ltp']["sdp"])
        def sdp(item: Item):  # 语义依存分析（树）
            ret = {
                'texts': item.texts,
            }
            try:
                cws, sdp = self._ltp.pipeline(
                    item.texts, tasks=["cws", "sdp"]).to_tuple()
                ret['sdp'] = sdp
                ret['cws'] = cws
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

        @self._app.post(config["route_path"]['ltp']["sdpg"])
        def sdpg(item: Item):  # 语义依存分析（图）
            ret = {
                'texts': item.texts,
            }
            try:
                cws, sdpg = self._ltp.pipeline(
                    item.texts, tasks=["cws", "sdpg"]).to_tuple()
                ret['sdpg'] = sdpg
                ret['cws'] = cws
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

        @self._app.post(config["route_path"]['ltp']["all"])
        def all(item: Item):  # 语义依存分析（图）
            ret = {
                'texts': item.texts,
                'all': {},
            }
            try:
                res = self._ltp.pipeline(item.texts, tasks=[
                    "cws", "pos", "ner", "srl", "dep", "sdp", "sdpg"]).to_tuple()
                ret['all'] = res
                return util.resultSuccess(ret)
            except Exception as e:
                print(e)
                return util.resultError(ret)

    def _init_sys(self):
        @self._app.post(config["route_path"]['sys']["login"])
        def login(item: LoginInfo):  # 登录
            try:
                return util.resultSuccess({
                    'userId': '1',
                    'username': 'vben',
                    'realName': 'Vben Admin',
                    'avatar': '',
                    'desc': 'manager',
                    'password': '123456',
                    'token': 'fakeToken1',
                    'homePath': '/dashboard/analysis',
                    'roles': [
                        {
                            'roleName': 'Super Admin',
                            'value': 'super',
                        },
                    ],
                })
            except Exception as e:
                print(e)
                return util.resultError('登录失败')

        @self._app.get(config["route_path"]['sys']["logout"])
        def logout():
            return util.resultSuccess(None, 'Token has been destroyed')

        @self._app.get(config["route_path"]['sys']["get_user_info"])
        def get_user_info(_t: int = 0):
            try:
                return util.resultSuccess({
                    'userId': '1',
                    'username': 'vben',
                    'realName': 'Vben Admin',
                    'avatar': '',
                    'desc': 'manager',
                    'password': '123456',
                    'token': 'fakeToken1',
                    'homePath': '/dashboard/analysis',
                    'roles': [
                        {
                            'roleName': 'Super Admin',
                            'value': 'super',
                        },
                    ],
                })
            except Exception as e:
                print(e)
                return util.resultError('登录失败')

        @self._app.get(config["route_path"]['sys']["get_prem_code"])
        def get_prem_code():
            return util.resultSuccess(['1000', '3000', '5000'])

        @self._app.get(config["route_path"]['sys']["get_menu_list"])
        def get_prem_code():
            return util.resultSuccess(util.menu_config())

    def run(self, host: str = config["default_host"], port: Union[int, str] = config["default_port"]):
        uvicorn.run(self._app, host=host, port=port)


def run_server(model_path: str, dict_path: str = None, max_window: int = int(config["default_max_window"]),
               host: str = config["default_host"], port: Union[int, str] = config["default_port"]):
    Server(model_path, dict_path=dict_path,
           max_window=max_window).run(host=host, port=port)


def run():
    Fire(run_server)
