from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter, Request
import db_session
from models import Vacancy
from db_model import Vacancy as db_vacancy
from parser import get_vacancy

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
router = APIRouter()

@router.post("/get_vacancies", response_model=list[Vacancy])
def get_vacancies(title: str, salary: int = 0, from_four_to_six_hours_in_a_day: bool = False,
                employment_part: bool = False,
                start_after_sixteen: bool = False,
                only_saturday_and_sunday: bool = False,
                employment_project: bool = False,
                not_required_or_not_specified: bool = False,
                higher: bool = False,
                special_secondary: bool = False,
                noExperience: bool = False,
                between1And3: bool = False,
                between3And6: bool = False,
                moreThan6: bool = False):
    get_vacancy(title,
                salary,
                from_four_to_six_hours_in_a_day,
                employment_part,
                start_after_sixteen,
                only_saturday_and_sunday,
                employment_project,
                not_required_or_not_specified,
                higher,
                special_secondary,
                noExperience,
                between1And3,
                between3And6,
                moreThan6)
    vacancy_list = list()
    db_session.global_init("Vacancy.db")
    db_sess = db_session.create_session()
    for vacancy_from_db in db_sess.query(db_vacancy).all():
        vacancy = Vacancy(
            id=vacancy_from_db.id,
            title=vacancy_from_db.title,
            experience=vacancy_from_db.experience,
            work_hours=vacancy_from_db.work_hours,
            salary=vacancy_from_db.salary
        )
        vacancy_list.append(vacancy)
    return vacancy_list

app.include_router(router)
templates = Jinja2Templates(directory='frontend')

@app.get('/search')
def get_base_page(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})
