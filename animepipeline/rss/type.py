from datetime import datetime
from typing import Union

from pydantic import AnyUrl, BaseModel


class TorrentInfo(BaseModel):
    name: str
    translation: str
    bangumi: Union[str, AnyUrl]
    episode: int
    title: str
    link: Union[str, AnyUrl]
    hash: str
    pub_date: datetime
    size: str
