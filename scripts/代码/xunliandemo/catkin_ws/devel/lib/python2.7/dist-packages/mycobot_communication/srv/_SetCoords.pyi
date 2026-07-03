import types
import typing

import genpy

class SetCoordsRequest(genpy.Message):
    _md5sum: str
    _type: str
    _has_header: bool
    _full_text: str
    __slots__: typing.List[str]
    _slot_types: typing.List[str]

    # Fields
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float
    speed: int
    model: int

    def __init__(
        self,
        x: float = ...,
        y: float = ...,
        z: float = ...,
        rx: float = ...,
        ry: float = ...,
        rz: float = ...,
        speed: int = ...,
        model: int = ...,
        *args: typing.Any,
        **kwds: typing.Any,
    ) -> None: ...
    def _get_types(self) -> typing.List[str]: ...
    def serialize(self, buff: typing.BinaryIO) -> None: ...
    def deserialize(self, str: bytes) -> SetCoordsRequest: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> SetCoordsRequest: ...

class SetCoordsResponse(genpy.Message):
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
    def deserialize(self, str: bytes) -> SetCoordsResponse: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> SetCoordsResponse: ...

class SetCoords(object):
    _type: str
    _md5sum: str
    _request_class = SetCoordsRequest
    _response_class = SetCoordsResponse
