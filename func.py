from __future__ import annotations

from uuid import UUID
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from litestar import get
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from litestar.controller import Controller
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Parameter
from litestar.repository.filters import LimitOffset

from models import GuestsModel
from pydantic_models import Guests
from sqlalchemy.ext.asyncio import AsyncSession


class GuestsRepository(SQLAlchemyAsyncRepository[GuestsModel]):
    model_type = GuestsModel
    
def limitoffsetpagination(
    current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False,
    ),
) -> LimitOffset:
    return LimitOffset(page_size, page_size * (current_page - 1))
async def guestsrepo(db_session: AsyncSession) -> GuestsRepository:
    return GuestsRepository(session=db_session)

async def guestsdetailsrepo(db_session: AsyncSession) -> GuestsRepository:
    return GuestsRepository(
        statement=select(GuestsModel).options(selectinload(GuestsModel.invited)),
        session=db_session,
    )  
    


class GuestsController(Controller):
    dependencies = {"guests_repo": Provide(guestsrepo)}
    
    @get(path="/")
    async def page(self) -> str:
        return "Пупупу"  
    
    @get(path="/guests")
    async def list_guests(
        self, guests_repo: GuestsRepository, limit_offset: LimitOffset,
    ) -> OffsetPagination[Guests]:
        results, total = await guests_repo.list_and_count(limit_offset)
        type_adapter = TypeAdapter(list[Guests])
        return OffsetPagination[Guests](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )         
        
    @get(path="/guests/{guests_id:uuid}", dependencies={"guests_repo": Provide(guestsdetailsrepo)})
    async def get_guest(
    self, guests_repo: GuestsRepository, guests_id: UUID = Parameter(title="Guest ID",),
    ) -> Guests:
        obj = await guests_repo.get(guests_id)
        return Guests.model_validate(obj)

    