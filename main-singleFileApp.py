from enum import Enum
import re, json
from typing import Annotated, Literal
from uuid import UUID
import uuid
from fastapi import Cookie, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field, computed_field

class MyCoolModel(str, Enum):
    foo = "foo_gw"
    bar = "barbasol"
    baz = "bazBall"
    dickie = "dickiePants"

class Item(BaseModel):
    name: Annotated[str, Field(description="Name of the item", examples=["My cool item"])]
    id: Annotated[UUID, Field(description="The UUID of the item")] = uuid.uuid4()
    description: Annotated[str | None, Field(description="Item description")] = None
    price: Annotated[float, Field(description="Price, tax excluded")]
    tax: Annotated[float | None, Field(description="Taxation rate")] = None
    @computed_field
    @property
    def price_with_tax(self) -> float | None:
        return round(self.price * (1 + self.tax), 2) if self.tax else None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "My other cool item",
                    "description": "Another worthwhile item that you'll want in your Easter basket 🐰 this year!",
                    "price": 3.50,
                    "tax": 0.09,
                    "price_with_tax": 3.82
                },
                {
                    "name": "My cool item",
                    "description": "Worthwhile item that you'll want to have under your Christmas tree 🎄 this year!",
                    "price": 99.95,
                    "tax": 0.05,
                    "price_with_tax": 104.95
                }
            ]
        }
    }

class FilterParams(BaseModel):
    limit: int = Field(default=10, description="Limit the number of items to return", example=[5,77], gt=0, le=100)
    offset: int = Field(default=0, description="Offset the items to return", example=5, ge=0)
    order_by: Literal["created_at", "updated_at"] = Field(default="created_at", description="Order the items by a specific field")
    tags: list[str] = Field(default=[], description="Filter items by tags")

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/items")
async def read_items(skip: Annotated[int, Query(ge=0, le=5)] = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items_filterExample")
async def read_items_filterExample(filter_query: Annotated[FilterParams, Query(description="Filter items", example={"limit": 5, "offset": 2, "order_by": "updated_at", "tags": ["foo", "bar"]})]):
    return filter_query

@app.get("/items_CookieExample")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

@app.post("/items")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        item_dict.update({"price_with_tax": round(item.price * (1 + item.tax), 2)})
    return item_dict

@app.get("/items/{item_id}")
async def read_item(item_id: Annotated[str, Path(title="The ID of the item to get")], q: Annotated[str | None, Query(min_length=3, max_length=50)] = None, full: bool = False):
    item = {"item_id": item_id}
    if q: item["q"] = q
    if full:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q: result.update({"q": q})
    return result

@app.get(path="/users/me")
async def read_user_me():
    return {"user_id": "current_foo"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    if user_id != "current_foo":
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found!")
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def read_model(model_name: MyCoolModel):
    # message = "Deep Learning FooTW!" if model_name is MyCoolModel.foo else (
    #     "LeCNN all the bars!" if model_name.value == "barbasol" else f"Default enum value: {model_name.value}"
    # )
    match model_name:
        case MyCoolModel.foo: message = "Deep Learning FooTW!"
        case MyCoolModel.bar: message = "LeCNN all the bars!"
        case _: message = f"Default enum name: {model_name.name}"
    return {"model_name": model_name, "message": message}

## make routes' paths case-insensitive; found at https://github.com/fastapi/fastapi/issues/826
for route in app.router.routes:
    # if isinstance(route, Route):
    route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)