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

CONFIG_PATH = "config.yml"

with open(os.path.join(os.path.dirname(__file__), CONFIG_PATH)) as file:
    config = yaml.safe_load(file.read())


class Item(BaseModel):
    texts: List[str]


class Words(BaseModel):
    words: List[str]
    max_window: int = 4


class Server:
    def __init__(self, model_path: str, dict_path: str = None, max_window: int = 4):
        self._app = FastAPI()
        self._ltp = LTP()
        self._stn_split = StnSplit()
        self
        if dict_path:
            self._ltp.init_dict(path=dict_path, max_window=max_window)
        self._init()

    def _init(self):
        @self._app.post(config["route_path"]["sent_split"])
        def stn_split(item: Item):  # 分句
            ret = {
                'texts': item.texts,
                'res': [],
                "status": 0
            }
            try:
                res = self._ltp._stn_split.split(item.texts)
                ret['res'] = res
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["add_words"])
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

        @self._app.post(config["route_path"]["seg"])
        def seg(item: Item):  # 分词
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
            }
            try:
                cws = self._ltp.pipeline(
                    item.texts, tasks=['cws']).to_tuple()
                ret['res'] = cws
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["pos"])
        def pos(item: Item):  # 词性标注
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
                'seg': []
            }
            try:
                cws, pos = self._ltp.pipeline(
                    item.texts, tasks=["cws", "pos"]).to_tuple()
                ret['res'] = pos
                ret['seg'] = cws
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["ner"])
        def ner(item: Item):  # 命名实体识别
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
                'seg': []
            }
            try:
                cws, ner = self._ltp.pipeline(
                    item.texts, tasks=["cws", "ner"]).to_tuple()
                ret['res'] = ner
                ret['seg'] = cws

            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["srl"])
        def srl(item: Item):  # 语义角色标注
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
                'seg': []
            }
            try:
                cws, srl = self._ltp.pipeline(
                    item.texts, tasks=["cws", "srl"]).to_tuple()
                ret['res'] = srl
                ret['seg'] = cws
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["dep"])
        def dep(item: Item):  # 依存句法分析
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
                'seg': []
            }
            try:
                cws, dep = self._ltp.pipeline(
                    item.texts, tasks=["cws", "dep"]).to_tuple()
                ret['res'] = dep
                ret['seg'] = cws
            except Exception as e:
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["sdp"])
        def sdp(item: Item):  # 语义依存分析（树）
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
                'seg': []
            }
            try:
                cws, sdp = self._ltp.pipeline(
                    item.texts, tasks=["cws", "sdp"]).to_tuple()
                ret['res'] = sdp
                ret['seg'] = cws
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["sdpg"])
        def sdpg(item: Item):  # 语义依存分析（图）
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
                'seg': []
            }
            try:
                cws, sdpg = self._ltp.pipeline(
                    item.texts, tasks=["cws", "sdpg"]).to_tuple()
                ret['res'] = sdpg
                ret['seg'] = cws
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

        @self._app.post(config["route_path"]["all"])
        def all(item: Item):  # 语义依存分析（图）
            ret = {
                'status': 0,
                'texts': item.texts,
                'res': [],
                'seg': [],
                'all': {},
            }
            try:
                res = self._ltp.pipeline(item.texts, tasks=[
                    "cws", "pos", "ner", "srl", "dep", "sdp", "sdpg"]).to_tuple()
                ret['all'] = res
            except Exception as e:
                print(e)
                ret['status'] = 1
            return ret

    def run(self, host: str = config["default_host"], port: Union[int, str] = config["default_port"]):
        uvicorn.run(self._app, host=host, port=port)


def run_server(model_path: str, dict_path: str = None, max_window: int = int(config["default_max_window"]),
               host: str = config["default_host"], port: Union[int, str] = config["default_port"]):
    Server(model_path, dict_path=dict_path,
           max_window=max_window).run(host=host, port=port)


def run():
    Fire(run_server)
