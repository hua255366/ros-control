import types
import typing

import genpy

class SetAnglesRequest(genpy.Message):
    _md5sum: str
    _type: str
    _has_header: bool
    _full_text: str
    __slots__: typing.List[str]
    _slot_types: typing.List[str]

    # Fields
    joint_1: float
    joint_2: float
    joint_3: float
    joint_4: float
    joint_5: float
    joint_6: float
    speed: int

    def __init__(
        self,
        joint_1: float = ...,
        joint_2: float = ...,
        joint_3: float = ...,
        joint_4: float = ...,
        joint_5: float = ...,
        joint_6: float = ...,
        speed: int = ...,
        *args: typing.Any,
        **kwds: typing.Any,
    ) -> None: ...
    def _get_types(self) -> typing.List[str]: ...
    def serialize(self, buff: typing.BinaryIO) -> None: ...
    def deserialize(self, str: bytes) -> SetAnglesRequest: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> SetAnglesRequest: ...

class SetAnglesResponse(genpy.Message):
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
    def deserialize(self, str: bytes) -> SetAnglesResponse: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> SetAnglesResponse: ...

class SetAngles(object):
    _type: str
    _md5sum: str
    _request_class = SetAnglesRequest
    _response_class = SetAnglesResponse
