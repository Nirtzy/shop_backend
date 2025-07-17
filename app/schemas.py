from pydantic import BaseModel, Field
from typing import Optional

class InfoQueryParams(BaseModel):
    name: Optional[str] = Field(None, description="Название продукта для фильтрации")
    category: Optional[str] = Field(None, description="Категория продукта для фильтрации")
