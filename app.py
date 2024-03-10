from __future__ import annotations
from litestar import Litestar
from litestar.contrib.sqlalchemy.base import UUIDBase
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from litestar.di import Provide
from func import GuestsController, limitoffsetpagination
from db import db_config

async def start() -> None:
    async with db_config.get_engine().begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)

app = Litestar(
    route_handlers=[GuestsController],
    on_startup=[start],
    plugins=[SQLAlchemyPlugin(db_config)],  
    dependencies={"limit_offset": Provide(limitoffsetpagination, sync_to_thread=False)}
)
