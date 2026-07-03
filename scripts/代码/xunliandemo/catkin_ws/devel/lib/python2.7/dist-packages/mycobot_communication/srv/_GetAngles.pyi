import types
import typing

import genpy

class GetAnglesRequest(genpy.Message):
    _md5sum: str
    _type: str
    _has_header: bool
    _full_text: str
    __slots__: typing.List[str]
    _slot_types: typing.List[str]

    def __init__(self, *args: typing.Any, **kwds: typing.Any) -> None: ...
    def _get_types(self) -> typing.List[str]: ...
    def serialize(self, buff: typing.BinaryIO) -> None: ...
    def deserialize(self, str: bytes) -> GetAnglesRequest: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> GetAnglesRequest: ...

class GetAnglesResponse(genpy.Message):
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

    def __init__(
        self,
        joint_1: float = ...,
        joint_2: float = ...,
        joint_3: float = ...,
        joint_4: float = ...,
        joint_5: float = ...,
        joint_6: float = ...,
        *args: typing.Any,
        **kwds: typing.Any,
    ) -> None: ...
    def _get_types(self) -> typing.List[str]: ...
    def serialize(self, buff: typing.BinaryIO) -> None: ...
    def deserialize(self, str: bytes) -> GetAnglesResponse: ...
    def serialize_numpy(self, buff: typing.BinaryIO, numpy: types.ModuleType) -> None: ...
    def deserialize_numpy(self, str: bytes, numpy: types.ModuleType) -> GetAnglesResponse: ...

class GetAngles(object):
    _type: str
    _md5sum: str
    _request_class = GetAnglesRequest
    _response_class = GetAnglesResponse
