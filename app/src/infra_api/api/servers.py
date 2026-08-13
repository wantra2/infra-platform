from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Server
from ..schemas import ServerCreate, ServerResponse, ServerUpdate

router = APIRouter(
    prefix="/api/v1/servers",
    tags=["servers"],
)


@router.get(
    "",
    response_model=list[ServerResponse],
)
def list_servers(
    db: Session = Depends(get_db),
) -> list[Server]:
    result = db.execute(
        select(Server).order_by(Server.id)
    )

    return list(result.scalars().all())


@router.get(
    "/{server_id}",
    response_model=ServerResponse,
)
def get_server(
    server_id: int,
    db: Session = Depends(get_db),
) -> Server:
    server = db.get(Server, server_id)

    if server is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )

    return server


@router.post(
    "",
    response_model=ServerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_server(
    payload: ServerCreate,
    db: Session = Depends(get_db),
) -> Server:
    existing = db.execute(
        select(Server).where(
            Server.hostname == payload.hostname
        )
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hostname already exists",
        )

    server = Server(**payload.model_dump())

    db.add(server)
    db.commit()
    db.refresh(server)

    return server


@router.patch(
    "/{server_id}",
    response_model=ServerResponse,
)
def update_server(
    server_id: int,
    payload: ServerUpdate,
    db: Session = Depends(get_db),
) -> Server:
    server = db.get(Server, server_id)

    if server is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(server, field, value)

    db.commit()
    db.refresh(server)

    return server


@router.delete(
    "/{server_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_server(
    server_id: int,
    db: Session = Depends(get_db),
) -> None:
    server = db.get(Server, server_id)

    if server is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found",
        )

    db.delete(server)
    db.commit()
