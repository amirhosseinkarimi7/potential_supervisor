from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

from fastapi.staticfiles import StaticFiles


from fastapi import FastAPI, Depends, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

import models
from models import person
from database import engine, SessionLocal


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Person_Req(BaseModel):
    uid: int
    uni: str
    dept: str
    name: str
    ra: str
    pub: str
    email: str


db_dep = Annotated[Session, Depends(get_db)]


# API that shows all of the entries in the database
@app.get("/people/")
async def home_page(request: Request, db: db_dep):
    people = db.query(person).all()
    return templates.TemplateResponse(
        "index2.html", {"request": request, "data": people}
    )


# CRUD functionality
# create a new entry to the database using ID
@app.post("/people/{person_id}", status_code=status.HTTP_201_CREATED)
async def create_new_entry(db: db_dep, person_req: Person_Req):
    new_person = person(**person_req.model_dump())
    db.add(new_person)
    db.commit()


# reading an entry
@app.get("/people/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_entry(db:db_dep,person_request: Person_Req, person_id: int = Path(gt=0)):
    req = db.query(person).filter(person.uid == person_id).first()
    if req is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person you are looking for with the id of {person_id} not found in the database",
        )

# updating an entry
@app.put("/people/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_person(
    db: db_dep, person_request: Person_Req, person_id: int = Path(gt=0)
):
    req = db.query(person).filter(person.uid == person_id).first()
    if req is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person you are looking for with the id of {person_id} not found in the database",
        )

    # Update fields from request
    for var, value in vars(person_request).items():
        setattr(req, var, value) if value else None

    db.commit()


# deleting an entru
@app.delete("/people/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(
    db: db_dep, person_request: Person_Req, person_id: int = Path(gt=0)
):
    req = db.query(person).filter(person.uid == person_id).first()
    if req is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person you are looking for with the id of {person_id} not found in the database",
        )
    db.delete(req)
    db.commit()
