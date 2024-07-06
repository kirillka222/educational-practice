from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Query
import db_session
from models import Vacancy
from db_model import Vacancy as db_vacancy
from parser import get_vacancy

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='frontend')

@app.get("/get_vacancies", response_model=list[Vacancy])
def get_vacancies(request: Request, text: str = Query(default=''),
                  salary: str = Query(default=''),
                  experience: list = Query(default=[]),
                  schedule: list = Query(default=[]),
                  employment: list = Query(default=[]),
                  education: list = Query(default=[])):
    get_vacancy(text, salary=salary, experience=experience, schedule=schedule, employment=employment, education=education)
    vacancy_list = list()
    db_session.global_init("Vacancy.db")
    db_sess = db_session.create_session()
    for vacancy_from_db in db_sess.query(db_vacancy).all():
        vacancy = Vacancy(
            id=vacancy_from_db.id,
            title=vacancy_from_db.title,
            experience=vacancy_from_db.experience,
            salary=vacancy_from_db.salary,
        )
        vacancy_list.append(vacancy)
    return templates.TemplateResponse('main.html', {"request": request, "data": vacancy_list})


@app.get('/search')
def get_search(request: Request):
    get_vacancy(text='',salary='', experience=[], schedule=[], employment=[], education=[])
    vacancy_list = []
    db_session.global_init("Vacancy.db")
    db_sess = db_session.create_session()
    for vacancy_from_db in db_sess.query(db_vacancy).all():
        vacancy = Vacancy(
            id=vacancy_from_db.id,
            title=vacancy_from_db.title,
            experience=vacancy_from_db.experience,
            salary=vacancy_from_db.salary
        )
        vacancy_list.append(vacancy)
    return templates.TemplateResponse('index.html', {"request": request, "data": vacancy_list})
