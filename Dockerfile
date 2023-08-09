# syntax docker/dockerfile:1.2
# Base user uid / gid keep 1000 on prod, align with your user on dev
ARG USER_UID=1000
ARG USER_GID=1000

FROM python:3.11

# install gettext-tools
RUN apt-get update && apt-get -y install gettext

ARG USER_UID
ARG USER_GID

WORKDIR /code
RUN groupadd -g $USER_GID off && \
    useradd -u $USER_UID -g off -m off && \ 
    mkdir -p /home/off && \ 
    chown off:off -R /code /home/off

COPY --chown=off:off ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

USER off:off
COPY --chown=off:off ./app /code/app
COPY --chown=off:off ./i18n /code/i18n
COPY --chown=off:off ./template /code/template

# format language files
RUN find i18n -name \*.po -execdir msgfmt knowledge-panel.po -o knowledge-panel.mo \;


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
