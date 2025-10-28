"""pytest 配置"""

import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any, Optional

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def _ensure_module(name: str) -> ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = ModuleType(name)
        sys.modules[name] = module
    return module


# ---- Hyperliquid SDK Stubs (用于测试环境) ----
hyperliquid_module = _ensure_module("hyperliquid")
api_module = _ensure_module("hyperliquid.api")
exchange_module = _ensure_module("hyperliquid.exchange")
info_module = _ensure_module("hyperliquid.info")
utils_module = _ensure_module("hyperliquid.utils")
constants_module = _ensure_module("hyperliquid.utils.constants")
signing_module = _ensure_module("hyperliquid.utils.signing")
types_module = _ensure_module("hyperliquid.utils.types")
websocket_module = _ensure_module("hyperliquid.websocket_manager")


class _API:  # pragma: no cover - 简易桩实现
    def __init__(self, *args, **kwargs):
        pass


api_module.API = getattr(api_module, "API", _API)


class _Exchange:  # pragma: no cover - 简易桩实现
    def __init__(self, *args, **kwargs):
        pass


exchange_module.Exchange = getattr(exchange_module, "Exchange", _Exchange)


class _Info:  # pragma: no cover - 简易桩实现
    def __init__(self, *args, **kwargs):
        pass


info_module.Info = getattr(info_module, "Info", _Info)

constants_module.MAINNET_API_URL = getattr(
    constants_module, "MAINNET_API_URL", "https://api.mock.hyperliquid"
)
constants_module.TESTNET_API_URL = getattr(
    constants_module, "TESTNET_API_URL", "https://api.mock.hyperliquid"
)


def _order_request_to_order_wire(order, asset):  # pragma: no cover - 测试桩
    return order


def _order_wires_to_order_action(wires, _builder):  # pragma: no cover - 测试桩
    return {"orders": wires}


def _sign_l1_action(*args, **kwargs):  # pragma: no cover - 测试桩
    return "signed"


signing_module.order_request_to_order_wire = getattr(
    signing_module, "order_request_to_order_wire", _order_request_to_order_wire
)
signing_module.order_wires_to_order_action = getattr(
    signing_module, "order_wires_to_order_action", _order_wires_to_order_action
)
signing_module.sign_l1_action = getattr(
    signing_module, "sign_l1_action", _sign_l1_action
)


class _Cloid(str):  # pragma: no cover - 简易桩实现
    pass


types_module.Any = getattr(types_module, "Any", Any)
types_module.Callable = getattr(types_module, "Callable", Callable)
types_module.Cloid = getattr(types_module, "Cloid", _Cloid)
types_module.List = getattr(types_module, "List", list)
types_module.Meta = getattr(types_module, "Meta", dict)
types_module.Optional = getattr(types_module, "Optional", Optional)
types_module.SpotMeta = getattr(types_module, "SpotMeta", dict)
types_module.SpotMetaAndAssetCtxs = getattr(types_module, "SpotMetaAndAssetCtxs", list)
types_module.Subscription = getattr(types_module, "Subscription", dict)
types_module.cast = getattr(types_module, "cast", lambda typ, val: val)


class _WebsocketManager:  # pragma: no cover - 简易桩实现
    def __init__(self, *args, **kwargs):
        pass

    def start(self):  # pragma: no cover - 简易桩实现
        pass

    def stop(self):  # pragma: no cover - 简易桩实现
        pass


websocket_module.WebsocketManager = getattr(
    websocket_module, "WebsocketManager", _WebsocketManager
)


# ---- FastMCP Stub ----
fastmcp_module = _ensure_module("fastmcp")


class _FastMCP:  # pragma: no cover - 简易桩实现
    def __init__(self, name: str):
        self.name = name

    def tool(self, func):
        return func

    def run_async(self, *args, **kwargs):
        raise RuntimeError("FastMCP stub does not support run_async in tests")

    def run(self, *args, **kwargs):
        raise RuntimeError("FastMCP stub does not support run in tests")


fastmcp_module.FastMCP = getattr(fastmcp_module, "FastMCP", _FastMCP)


# ---- eth_account Stub ----
eth_account_module = _ensure_module("eth_account")


class _AccountStub:  # pragma: no cover - 简易桩实现
    @staticmethod
    def from_key(private_key: str):
        class _Wallet:  # pragma: no cover - 简易桩实现
            address = "0xSTUB_ACCOUNT"

        return _Wallet()


eth_account_module.Account = getattr(eth_account_module, "Account", _AccountStub)
