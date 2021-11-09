#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import socket
from consul import Consul, Check


class ConsulUtil(object):
    """
    ConsulUtil 提供 python 对 consul 中服务相关的简洁操作，如注册一个本地服务到 consul，获取已经注册到 consul 中的服务地址等。

    :param host: consul 服务地址
    :param port: consul 端口

    Example1: 获取服务 demo 的所有地址：
    import consul_util
    print(consul_util.get_all_address("demo"))

    Example2: 注册本地服务 demo:1234 到 consul
    from consul_util import ConsulUtil
    c = ConsulUtil()
    c.register("demo", 1234)
    """

    def __init__(self, host="127.0.0.1", port=8500):
        self.host = host
        self.port = port
        self._c = Consul(host, port)

    def get_all_address(self, service_name: str, tags="") -> list:
        """
        从 consul 中获取对应服务的连接地址
        :param service_name: 服务名, 如 "offer-api"返回所有地址, "offer-api:v2.3.0"只返回 v2.3.0 版本的连接地址
        :param tags: 指定版本号，如果这里指定版本，则不会从 `service_name` 中解析 tag
        :return: 该服务的所有的连接地址,如["127.0.0.1:1234", "127.0.0.1:3456"]
        """
        return self._get_address_with_tag(service_name, tags)

    def get_address(self, service_name: str, tag="") -> str:
        """
        返回服务的单个连接地址
        :param service_name: 服务名, 如 "offer-api"表示从所有地址中取一个, "offer-api:v2.3.0"只返回 v2.3.0 版本的连接地址中的一个
        :param tag: 版本号
        :return: 该服务的一个连接地址，！！！如果没有连接地址，则返回该服务名！！！(和 Golang 基础库中保持一致)
        """
        services = self.get_all_address(service_name, tag)
        if services is None or len(services) == 0:
            return service_name
        return services[0]

    def register(self, service_name: str, port: int, tag=""):
        """
        将一个服务注册到 consul 中
        :param service_name: 服务名，如 "offer-api"，"offer-api:v2.3.0"
        :param port: 端口号，如 34657
        :param tag: 版本号，如 v2.3.0
        :return: 成功时返回 None；失败时返回对应的错误信息
        """
        return self._register(service_name, port, tag)

    def unregister(self, service_name: str):
        """
        将服务所有版本从当前 agent 中取消注册
        :param service_name: 服务名，如 "offer-api"，"offer-api:v2.3.0"
        :return: 成功时返回 None；失败时返回对应的错误信息
        """
        return self._unregister(service_name)

    def _get_address(self, service_name):
        service, tag = self.split_tag(service_name)
        return self._get_address_with_tag(service, tag)

    def _get_address_with_tag(self, service_name, tag=""):
        service = service_name
        if tag == "":
            tag = None
            if service_name.find(":") > -1:
                service, tag = self.split_tag(service_name)
        _, value = self._c.health.service(service=service, tag=tag)
        if value is None or len(value) == 0:
            # 尝试从本地的 agent 中去获取，此时 tag 无效
            services = self._c.agent.services()
            return self._filter_agent_address(services, service_name)
        return self._filter_address(value)

    def _register(self, service_name, port, tag):
        print(service_name, port, tag)
        try:
            tags = None
            if tag != "":
                tags = [tag]
            service = service_name
            s, t = self.split_tag(service_name)
            if t and not tags:
                tags = [t]
                service = s
            self._c.agent.service.register(
                name=service, port=port, tags=tags,
                service_id=self.get_service_id(service, port),
                check=Check().tcp(self.host, port, "5s", "30s", "30s")
            )
            return None
        except Exception as e:
            return str(e)

    def _unregister(self, service_name):
        try:
            service_name, _ = self.split_tag(service_name)
            for idx, item in self._c.agent.services().items():
                if item.get("Service") == service_name:
                    self._c.agent.service.unregister(idx)
            return None
        except Exception as e:
            return str(e)

    @staticmethod
    def split_tag(service_name):
        tmp = service_name.split(":")
        if len(tmp) > 1:
            return tmp[0], tmp[1]
        return service_name, None

    @staticmethod
    def get_service_id(name, port):
        hostname = socket.gethostname().replace(".", "-")
        return "{}-{}-{}".format(name, port, hostname)

    @staticmethod
    def _filter_address(value):
        res = []
        for i in value:
            if i.get("Service") is None:
                continue
            address, port = i["Service"].get("Address") or "", i["Service"].get("Port") or 0
            if address == "" and i.get("Node") is not None:
                address = i["Node"].get("Address")
            if address == "" or port == 0:
                continue
            res.append("{}:{}".format(address, port))
        return res

    @staticmethod
    def _filter_agent_address(value, service):
        res = []
        for j, i in value.items():
            if i.get("Service") is None or i.get("Service") != service:
                continue
            if i.get("Port") == 0:
                continue
            res.append("{}:{}".format(i.get("Address") or "localhost", i.get("Port")))
        if len(res) == 0:
            return None
        return


default_consul = ConsulUtil()


def all_address(service_name, tag=""):
    """
    从 consul 中获取对应服务的连接地址
    :param service_name: 服务名, 如 "offer-api"返回所有地址, "offer-api:v2.3.0"只返回 v2.3.0 版本的连接地址
    :param tag: 指定版本号，如果这里指定版本，则不会从 `service_name` 中解析 tag
    :return: 该服务的所有的连接地址,如["127.0.0.1:1234", "127.0.0.1:3456"]
    """
    return default_consul.get_all_address(service_name, tag)


def one_address(service_name, tag=""):
    """
    返回服务的单个连接地址
    :param service_name: 服务名, 如 "offer-api"表示从所有地址中取一个, "offer-api:v2.3.0"只返回 v2.3.0 版本的连接地址中的一个
    :param tag: 版本号
    :return: 该服务的一个连接地址，！！！如果没有连接地址，则返回该服务名！！！(和 Golang 基础库中保持一致)
    """
    return default_consul.get_address(service_name, tag)


if __name__ == '__main__':
    c = ConsulUtil()


    def __register(*kwargs):
        print("register {} with port:{}, tags:{}".format(kwargs[0].service, kwargs[0].port, kwargs[0].tags))
        c.register(kwargs[0].service, kwargs[0].port, kwargs[0].tags)


    def __unregister(*kwargs):
        print("unregister {}".format(kwargs[0].service))
        c.unregister(kwargs[0].service)


    def __get_address(*kwargs):
        print(c.get_address(kwargs[0].service))


    import argparse

    parser = argparse.ArgumentParser(prog="consul_util")
    sub_parser = parser.add_subparsers(title="actions")

    register_parser = sub_parser.add_parser('register', help='register service to consul')
    register_parser.add_argument("service", type=str, help="service name")
    register_parser.add_argument("port", type=int, help="service port")
    register_parser.add_argument("--tags", type=list, help="service tags")
    register_parser.set_defaults(func=__register)

    de_register_parser = sub_parser.add_parser("unregister", help="unregister service")
    de_register_parser.add_argument("service", type=str, help="service name")
    de_register_parser.set_defaults(func=__unregister)

    get_address_parser = sub_parser.add_parser("get_address", help="get service address list")
    get_address_parser.add_argument("service", type=str, help="service name")
    get_address_parser.set_defaults(func=__get_address)

    args = parser.parse_args()
    args.func(args)

