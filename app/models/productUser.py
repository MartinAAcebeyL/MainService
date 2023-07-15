from sqlmodel import SQLModel, Field
from typing import Optional

class ProductUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    product_id: int

