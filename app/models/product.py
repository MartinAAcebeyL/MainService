from sqlmodel import SQLModel, Field
from typing import Optional


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str

    class Config:
        orm_mode = True
        tablename = "product"

    def save(self, session):
        session = next(session)
        print(self.title, self.image)
        product = Product(title=self.title, image=self.image)
        session.add(product)
        session.commit()
        return product
