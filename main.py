from fastapi import FastAPI, Body, Header, Request
from fastapi.responses import HTMLResponse, FileResponse, Response
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from jinja2 import Template
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
engine = create_engine('sqlite:///mydatabase.db', echo=True)
Base = declarative_base()

class Item(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=False)
    url = Column(String)
    name = Column(String)
    phone_number = Column(String)
    price = Column(String)
    description = Column(String)
    address = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class HtmlTemplate:
    template = """
    <!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" type="text/css" href="index.css">
</head>
<body>
    <div class="container">
        {% for item in items %}
        <div class="item">    
            <div class="item_image-wrapper">
                <img>
                <img>
            </div>
            <div class="item_url">
                {{ item.url }}
            </div>
            <div class="item_name">
                {{ item.name }}
            </div>
            <div class="item_price">
                {{ item.price }}
            </div>
            <div class="item_phone-number">
                {{ item.phone_number }}
            </div>
            <div class="item_address">
                {{ item.address }}
            </di
            <div class="item_description">
                {{ item.description }}
            </div>   
        </div>
        {% endfor %}
    </div>
</body>
</html>
    """

    def __init__(self, items):
        template = Template(self.template)
        self.html = template.render(items=items)
    pass




class DataItem(BaseModel):
    item_id: int
    url: str
    name: str
    phone_number: str
    price: str
    description: str
    address: str


@app.get("/")
async def read_root():
    items = session.query(Item).all()
    rendered_html = HtmlTemplate(items)
    html = rendered_html.html
    return HTMLResponse(content=html, status_code=200)

@app.get("/index.css")
async def read_root():
    path = "./index.css"
    return FileResponse(path)

@app.post("/add_item")
async def add_data_to_db(item: DataItem):
#async def add_data_to_db(request: DataItem = Body(...)):
    print(int(item.item_id))
    print(item.url)
    print(item.address)
    db_item = session.query(Item).filter_by(id=item.item_id).first()
    if not db_item:
        new_item = Item(id=item.item_id, url=item.url, name=item.name, phone_number=item.phone_number, price=item.price, description=item.description, address=item.address)
        try:
            session.add(new_item)
            session.commit()
        except Exception as e:
            session.rollback()
    print("success")
    return Response(status_code=200)

@app.get("/get_item")
async def get_item_from_db():
    return [*session.query(Item).all()]
    #return {"eee":"ok", "Gaead":"ok"}
    #return [i for i in data]
    new_item = Item(id = data["item_id"], url = data["url"])
    #session.add(new_item)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("ERRRRRRROOOOOOOOOOOOR")
    print(await request.body())
    print(exc)
    return JSONResponse(
        status_code=422,
        content={"message": "Ошибка валидации данных в теле запроса"},)



#if __name__ == '__main__':


