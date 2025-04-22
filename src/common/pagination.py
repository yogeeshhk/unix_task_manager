from typing import Generic, TypeVar, List, Optional

from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    total: int
    page: int
    page_size: int
    next_page: Optional[int]
    previous_page: Optional[int]
    total_pages: int
    items: List[T]
