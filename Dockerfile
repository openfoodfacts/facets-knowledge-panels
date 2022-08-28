
FROM python:3.9

# install gettext-tools
RUN apt-get update && apt-get -y install gettext

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./i18n /code/i18n
# format language files
RUN find i18n -name \*.po -execdir msgfmt knowledge-panel.po -o knowledge-panel.mo \;


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
