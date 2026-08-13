from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServerBase(BaseModel):
    hostname: str
    environment: str
    region: str
    status: str = "running"
    cpu: int
    memory_gb: int
    owner: str


class ServerCreate(ServerBase):
    pass


class ServerUpdate(BaseModel):
    hostname: str | None = None
    environment: str | None = None
    region: str | None = None
    status: str | None = None
    cpu: int | None = None
    memory_gb: int | None = None
    owner: str | None = None


class ServerResponse(ServerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
