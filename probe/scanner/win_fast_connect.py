"""
win_fast_connect.py — make a refused connect() fail at network speed on Windows.

WHY
---
When Windows receives an RST in answer to a SYN it does not fail connect(); it
waits ~500 ms and sends the SYN again, several times (measured on a customer
agent: 2.2 s to report one closed port that Linux reports in ~1 ms). A connect
scan therefore sees almost every closed port time out, records it `filtered`,
and only the slow cleanup pass finds out it was closed (`1110/1110` "ambiguous"
ports resolved on a 1,145-port sweep, 6.5 minutes instead of seconds).

Windows 8+ lets a socket opt out with the SIO_TCP_INITIAL_RTO ioctl:
MaxSynRetransmissions = TCP_INITIAL_RTO_NO_SYN_RETRANSMISSIONS. Python's
socket.ioctl() only accepts three control codes, so this calls WSAIoctl through
ctypes (standard library: nothing new ships).

Two Windows facts the values below encode (constants from mstcpip.h; the version
gate is the one OpenJDK ships for the same fix):
  * before Windows 10 RS3 (build 16299) the "no retransmissions" value is not
    recognised and reads as 255 retries, so those builds get 1 (the minimum);
  * 0 means "use the default", so it can never be used to mean "none".

Without OS retransmission one lost SYN reads as silence; the port scanner's own
retries and its cleanup pass already re-probe silence. Scan sockets only: the
agent's connection to the manager keeps the normal TCP behaviour.

Fail-safe: anything unexpected leaves the socket exactly as it was.
"""
from __future__ import annotations

import ctypes
import logging
import socket
import sys
from functools import lru_cache
from typing import Callable

LOG = logging.getLogger("scanner")

# mstcpip.h: #define SIO_TCP_INITIAL_RTO _WSAIOW(IOC_VENDOR,17)
#            IOC_IN 0x80000000 | IOC_VENDOR 0x18000000 | 17
SIO_TCP_INITIAL_RTO = 0x98000011
TCP_INITIAL_RTO_UNSPECIFIED_RTT = 0xFFFF        # (USHORT) -1: keep the system's RTT
TCP_INITIAL_RTO_NO_SYN_RETRANSMISSIONS = 0xFE   # (UCHAR) -2

WINDOWS_8_BUILD = 9200
WINDOWS_10_RS3_BUILD = 16299


class _InitialRtoParameters(ctypes.Structure):
    """TCP_INITIAL_RTO_PARAMETERS: { USHORT Rtt; UCHAR MaxSynRetransmissions; }"""
    _fields_ = [("Rtt", ctypes.c_ushort), ("MaxSynRetransmissions", ctypes.c_ubyte)]


#: (socket handle, control code, input bytes) -> 0 on success, else an error code.
Ioctl = Callable[[int, int, bytes], int]


def max_syn_retransmissions(build: int) -> int | None:
    """The MaxSynRetransmissions value this Windows build understands, or None
    when the ioctl does not exist (before Windows 8)."""
    if build >= WINDOWS_10_RS3_BUILD:
        return TCP_INITIAL_RTO_NO_SYN_RETRANSMISSIONS
    if build >= WINDOWS_8_BUILD:
        return 1
    return None


def payload(max_syn: int) -> bytes:
    """The exact input buffer WSAIoctl receives (4 bytes, C layout)."""
    return bytes(_InitialRtoParameters(TCP_INITIAL_RTO_UNSPECIFIED_RTT, max_syn))


def _windows_build() -> int:
    version = sys.getwindowsversion()          # type: ignore[attr-defined]
    real = getattr(version, "platform_version", None)
    return int(real[2] if real else version.build)


def _wsaioctl(handle: int, code: int, data: bytes) -> int:
    ws2 = ctypes.WinDLL("ws2_32", use_last_error=True)   # type: ignore[attr-defined]
    fn = ws2.WSAIoctl
    fn.argtypes = [ctypes.c_size_t, ctypes.c_ulong, ctypes.c_void_p, ctypes.c_ulong,
                   ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong),
                   ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = ctypes.c_int
    buf = ctypes.create_string_buffer(data, len(data))
    returned = ctypes.c_ulong(0)
    rc = fn(handle, code, buf, len(data), None, 0, ctypes.byref(returned), None, None)
    return 0 if rc == 0 else (ctypes.get_last_error() or -1)


@lru_cache(maxsize=1)
def _setting() -> int | None:
    """MaxSynRetransmissions for THIS machine, or None when it does not apply."""
    if sys.platform != "win32":
        return None
    try:
        return max_syn_retransmissions(_windows_build())
    except Exception:  # noqa: BLE001 — an unreadable version means "leave sockets alone"
        return None


_warned = False


def enable(sock: socket.socket, *, setting: int | None = None,
           ioctl: Ioctl | None = None) -> bool:
    """Opt this socket out of SYN retransmission. True when applied.

    Call before connect(). `setting` and `ioctl` are injectable for tests; by
    default they come from this machine (a no-op off Windows).
    """
    global _warned
    value = _setting() if setting is None else setting
    if value is None:
        return False
    try:
        rc = (ioctl or _wsaioctl)(sock.fileno(), SIO_TCP_INITIAL_RTO, payload(value))
    except Exception as exc:  # noqa: BLE001 — fail-safe: the socket stays as it was
        rc = exc
    if rc == 0:
        return True
    if not _warned:
        _warned = True
        LOG.warning("connect fast-fail unavailable (SIO_TCP_INITIAL_RTO: %s): closed "
                    "ports will take Windows' default ~2 s to report", rc)
    return False


def describe() -> dict:
    """What this machine does, for logs and `doctor`."""
    value = _setting()
    return {
        "applies": value is not None,
        "max_syn_retransmissions": value,
        "mode": ("none" if value == TCP_INITIAL_RTO_NO_SYN_RETRANSMISSIONS
                 else "one" if value == 1 else "default"),
    }
