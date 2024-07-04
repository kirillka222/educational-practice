from bs4 import BeautifulSoup as bs
import requests
import db_session
db_session.global_init("Vacancy.db")
from db_model import Vacancy


def get_vacancy(text, salary=0, experience=[], schedule=[], employment=[], education=[]):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    url = "https://hh.ru/search/vacancy?L_save_area=true&excluded_text=&area=113&salary=&currency_code=RUR&order_by=relevance&search_period=0&only_with_salary=true&hhtmFrom=vacancy_search_filter"
    hh_request = requests.get(url=url, headers=headers, params={
        "text": text,
        "salary": salary,
        "experience": experience,
        "schedule": schedule,
        "employment": employment,
        "education": education
    })
    parser = bs(hh_request.text, 'html.parser')
    info = parser.find_all('div', attrs={"class": "vacancy-search-item__card"})
    list_of_vacancy = []
    for vacancy in info:
        title = vacancy.find_next('span', attrs={"data-qa": "serp-item__title"})
        title = '' if title is None else title.text
        experience = vacancy.find_next('span', attrs={"data-qa": "vacancy-serp__vacancy-work-experience"})
        experience = '' if experience is None else experience.text
        salary = vacancy.find_next(name='span',
                                      attrs={'class': lambda tag: False if tag is None
                                      else 'compensation-text' in tag})
        salary = '' if salary is None else salary.text.replace('\u202f',' ').replace('\xa0',' ')
        list_of_vacancy += [(title, experience, salary)]

    db_sess = db_session.create_session()
    db_sess.query(Vacancy).delete()
    db_sess.commit()
    db_sess.close()
    for title, experience, salary in list_of_vacancy:
        db_sess = db_session.create_session()
        vac = Vacancy()
        vac.title = title
        vac.experience = experience
        vac.salary = salary
        db_sess.add(vac)
        db_sess.commit()
    return list_of_vacancy
