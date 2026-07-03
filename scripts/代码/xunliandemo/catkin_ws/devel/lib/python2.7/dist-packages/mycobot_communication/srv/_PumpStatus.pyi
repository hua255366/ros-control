import types
import typing

import genpy

class PumpStatusRequest(genpy.Message):
    _md5sum: str
    _type: str
    _has_header: bool
    _full_text: str
    __slots__: typing.List[str]
    _slot_types: typing.List[str]

    # Fields
    Status: bool

    def __init__(self, Status: bool = ..., *args: typing.Any, **kwds: typing.Any) -> None: ...
    def _get_types(self) -> typing.List[str]: ...
    def serialize(self, buff: typing.BinaryIO) -> None: ...
    def deserialize(self, str: bytes) -> PumpStatusRequest: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> PumpStatusRequest: ...

class PumpStatusResponse(genpy.Message):
    _md5sum: str
    _type: str
    _has_header: bool
    _full_text: str
    __slots__: typing.List[str]
    _slot_types: typing.List[str]

    # Fields
    Flag: bool

    def __init__(self, Flag: bool = ..., *args: typing.Any, **kwds: typing.Any) -> None: ...
    def _get_types(self) -> typing.List[str]: ...
    def serialize(self, buff: typing.BinaryIO) -> None: ...
    def deserialize(self, str: bytes) -> PumpStatusResponse: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> PumpStatusResponse: ...

class PumpStatus(object):
    _type: str
    _md5sum: str
    _request_class = PumpStatusRequest
    _response_class = PumpStatusResponse
