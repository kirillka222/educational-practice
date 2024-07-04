FROM python:3.11-slim

WORKDIR /vacancy_project

COPY . /vacancy_project

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]