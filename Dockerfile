FROM python:3.8

USER root
# https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password --gecos "Default user" --uid ${NB_UID} ${NB_USER}

# cython and libzmq3-dev needed atm to build pyzmq in 3.8
RUN apt-get update
RUN apt-get install -y tree libzmq3-dev
RUN apt-get install -y
COPY fonts /usr/share/fonts
RUN fc-cache -f

USER ${NB_USER}
ENV VIRTUAL_ENV=${HOME}/venv
RUN python3.8 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir cython==0.29.14 jupyter==1.0.0 rise==5.5.1 pytest==5.1.2

WORKDIR ${HOME}
COPY . ${HOME}

USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}
RUN mkdir -p ${VIRTUAL_ENV}/etc/jupyter/nbconfig/
RUN mv ${HOME}/.jupyter/rise.json ${VIRTUAL_ENV}/etc/jupyter/nbconfig/rise.json

RUN jupyter-nbextension install rise --py --sys-prefix
RUN jupyter-nbextension enable rise --py --sys-prefix
RUN jupyter --version
RUN jupyter --paths
