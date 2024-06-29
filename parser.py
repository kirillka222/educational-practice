from bs4 import BeautifulSoup as bs
import requests
import db_session
db_session.global_init("Vacancy.db")
from db_model import Vacancy

def get_vacancy(title, salary=0,
                from_four_to_six_hours_in_a_day = False,
                employment_part = False,
                start_after_sixteen = False,
                only_saturday_and_sunday = False,
                employment_project = False,
                not_required_or_not_specified = False,
                higher = False,
                special_secondary = False):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    if from_four_to_six_hours_in_a_day:
        part_time = f'part_time=from_four_to_six_hours_in_a_day&'
    else:
        part_time = ''
    part_time2 = 'part_time=employment_part&' if employment_part else ''
    part_time3 = 'part_time=start_after_sixteen&' if start_after_sixteen else ''
    part_time4 = 'part_time=only_saturday_and_sunday&' if only_saturday_and_sunday else ''
    part_time5 = 'part_time=employment_project&' if employment_project else ''
    education1 = 'education=not_required_or_not_specified&' if not_required_or_not_specified else ''
    education2 = 'education=higher&' if higher else ''
    education3 = 'education=special_secondary&' if special_secondary else ''
    hh_request = requests.get(f'https://hh.ru/search/vacancy?'
                              f'L_save_area=true&'
                              f'text={title}&'
                              f'excluded_text=&'
                              f'area=113&'
                              f'salary=&'
                              f'currency_code=RUR&'
                              f'experience=doesNotMatter&'
                              f'order_by=relevance&'
                              f'search_period=0&'
                              f'{part_time}&'
                              f'{part_time2}&'
                              f'{part_time3}&'
                              f'{part_time4}&'
                              f'{part_time5}&'
                              f'salary={salary}&'
                              f'items_on_page=100&'
                              f'{education1}&'
                              f'{education2}&'
                              f'{education3}&'
                              f'hhtmFrom=vacancy_search_filter', headers=headers)


    parser = bs(hh_request.text, 'html.parser')
    info = parser.find_all('div', attrs={"class": "vacancy-search-item__card"})
    list_of_vacancy = []
    for vacancy in info:
        title = vacancy.find_next('span', attrs={"data-qa": "serp-item__title"})
        title = '' if title is None else title.text
        experience = vacancy.find_next('span', attrs={"data-qa": "vacancy-serp__vacancy-work-experience"})
        experience = '' if experience is None else experience.text
        work_hours = vacancy.find_next('span', attrs={"data-qa": "vacancy-label-remote-work-schedule"})
        work_hours = '' if work_hours is None else work_hours.text
        salary = vacancy.find_next(name='span',
                                      attrs={'class': lambda tag: False if tag is None
                                      else 'compensation-text' in tag})
        salary = '' if salary is None else salary.text
        list_of_vacancy += [(title,experience,work_hours,salary)]


    for title,experience,work_hours,salary in list_of_vacancy:
        db_sess = db_session.create_session()
        vac = Vacancy()
        vac.title = title
        vac.experience = experience
        vac.work_hours = work_hours
        vac.salary = salary
        db_sess.add(vac) # запрос
        db_sess.commit() # выполнили запрос
    return list_of_vacancy
get_vacancy("python")


