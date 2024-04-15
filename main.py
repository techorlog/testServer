from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from jinja2 import Template

app = FastAPI()
engine = create_engine('sqlite:///mydatabase.db', echo=True)
Base = declarative_base()
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
async def add_data_to_db(data: dict = Body(...)):
    required_keys = ("item_id", "url", "name", "phone_number")
    is_data_valid = all(key in data for key in required_keys)
    if is_data_valid:
        item = session.query(Item).filter_by(id = data["item_id"]).first()
        if not item:
            new_item = Item(id=data["item_id"], url=data["url"], name=data["name"], phone_number=data["phone_number"])
            try:
                session.add(new_item)
                session.commit()
            except Exception as e:
                session.rollback()
        print("success")

@app.get("/get_item")
async def get_item_from_db():
    return [*session.query(Item).all()]
    #return {"eee":"ok", "Gaead":"ok"}
    #return [i for i in data]
    new_item = Item(id = data["item_id"], url = data["url"])
    #session.add(new_item)



class Item(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=False)
    #item_id = Column(String)
    url = Column(String)
    name = Column(String)
    phone_number = Column(String)
    #description
    #photo_set


#if __name__ == '__main__':


