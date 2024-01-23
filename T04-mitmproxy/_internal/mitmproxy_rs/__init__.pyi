from __future__ import annotations

from pathlib import Path
from typing import Awaitable, Callable, Any, Literal
from typing import final, overload, TypeVar


T = TypeVar("T")

# WireGuard

async def start_wireguard_server(
    host: str,
    port: int,
    private_key: str,
    peer_public_keys: list[str],
    handle_tcp_stream: Callable[[Stream], Awaitable[None]],
    handle_udp_stream: Callable[[Stream], Awaitable[None]],
) -> WireGuardServer: ...

@final
class WireGuardServer:
    def getsockname(self) -> tuple[str, int]: ...
    def close(self) -> None: ...
    async def wait_closed(self) -> None: ...
    def __repr__(self) -> str: ...

def genkey() -> str: ...
def pubkey(private_key: str) -> str: ...


# Local Redirector

async def start_local_redirector(
    handle_tcp_stream: Callable[[Stream], Awaitable[None]],
    handle_udp_stream: Callable[[Stream], Awaitable[None]],
) -> LocalRedirector: ...

@final
class LocalRedirector:
    @staticmethod
    def describe_spec(spec: str) -> None: ...
    def set_intercept(self, spec: str) -> None: ...
    def close(self) -> None: ...
    async def wait_closed(self) -> None: ...


# UDP

async def start_udp_server(
    host: str,
    port: int,
    handle_udp_stream: Callable[[Stream], Awaitable[None]],
) -> UdpServer: ...

@final
class UdpServer:
    def getsockname(self) -> tuple[str, int]: ...
    def close(self) -> None: ...
    async def wait_closed(self) -> None: ...
    def __repr__(self) -> str: ...

async def open_udp_connection(
    host: str,
    port: int,
    *,
    local_addr: tuple[str, int] | None = None,
) -> Stream: ...

# TCP / UDP

@final
class Stream:
    async def read(self, n: int) -> bytes: ...
    def write(self, data: bytes): ...
    async def drain(self) -> None: ...
    def write_eof(self): ...

    def close(self): ...
    def is_closing(self) -> bool: ...
    async def wait_closed(self) -> None: ...

    @overload
    def get_extra_info(self, name: Literal["transport_protocol"], default: None = None) -> Literal["tcp", "udp"]: ...
    @overload
    def get_extra_info(self, name: Literal["transport_protocol"], default: T) -> Literal["tcp", "udp"] | T: ...
    @overload
    def get_extra_info(self, name: Literal["peername", "sockname", "original_src", "original_dst", "remote_endpoint"], default: None = None) -> tuple[str, int]: ...
    @overload
    def get_extra_info(self, name: Literal["peername", "sockname", "original_src", "original_dst", "remote_endpoint"], default: T) -> tuple[str, int] | T: ...
    @overload
    def get_extra_info(self, name: Literal["pid"], default: None = None) -> int: ...
    @overload
    def get_extra_info(self, name: Literal["pid"], default: T) -> int | T: ...
    @overload
    def get_extra_info(self, name: Literal["process_name"], default: None = None) -> str: ...
    @overload
    def get_extra_info(self, name: Literal["process_name"], default: T) -> str | T: ...
    @overload
    def get_extra_info(self, name: str, default: Any) -> Any: ...

    def __repr__(self) -> str: ...


# Certificate Installation

def add_cert(pem: str) -> None: ...
def remove_cert() -> None: ...


# Process Info

def active_executables() -> list[Process]: ...
def executable_icon(path: Path | str) -> bytes: ...

@final
class Process:
    @property
    def executable(self) -> str: ...
    @property
    def display_name(self) -> str: ...
    @property
    def is_visible(self) -> bool: ...
    @property
    def is_system(self) -> bool: ...
