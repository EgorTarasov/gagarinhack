from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommunitiesRequest(_message.Message):
    __slots__ = ("ids", "k")
    IDS_FIELD_NUMBER: _ClassVar[int]
    K_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    k: int
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., k: _Optional[int] = ...) -> None: ...

class Community(_message.Message):
    __slots__ = ("name", "score")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    name: str
    score: float
    def __init__(self, name: _Optional[str] = ..., score: _Optional[float] = ...) -> None: ...

class CommunitiesResponse(_message.Message):
    __slots__ = ("communities",)
    COMMUNITIES_FIELD_NUMBER: _ClassVar[int]
    communities: _containers.RepeatedCompositeFieldContainer[Community]
    def __init__(self, communities: _Optional[_Iterable[_Union[Community, _Mapping]]] = ...) -> None: ...
