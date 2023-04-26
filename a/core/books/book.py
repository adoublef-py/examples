from uuid import UUID, uuid4
from pydantic import BaseModel, confloat, constr


class Book(BaseModel):  # this is the domain model
    id: UUID | None = uuid4()
    title: str
    author: constr(min_length=1, regex="[A-Za-z ,.'-]+$")
    price: confloat(gt=0)
    year: int | None = None
