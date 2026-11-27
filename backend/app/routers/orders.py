from __future__ import annotations

from fastapi import APIRouter
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.db import db
from app.services import order_service
from app.services.common import rows

router = APIRouter(tags=["启停单"])


class OrderIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    pod_id: int = Field(validation_alias=AliasChoices("pod_id", "podId", "pod"))
    action: str = Field(validation_alias=AliasChoices("action", "动作"))
    target_image_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("target_image_id", "targetImageId", "image_id"),
    )


@router.get("/启停单")
def list_orders():
    with db() as conn:
        return rows(conn.execute("SELECT * FROM start_orders ORDER BY id DESC"))


@router.post("/启停单")
def create_order(body: OrderIn):
    return order_service.create_order(
        pod_id=body.pod_id,
        action=body.action,
        target_image_id=body.target_image_id,
    )
