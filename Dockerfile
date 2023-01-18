FROM alpine:latest

RUN apk add --no-cache zsh git curl python3 sqlite make py3-pip

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

RUN pip install pytermgui

ENV SHELL /usr/bin/zsh

WORKDIR /app

CMD zsh
