# see https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
# https://pythonspeed.com/articles/multi-stage-docker-python/
# https://pythonspeed.com/docker/
#
# jupyter --paths
#config:
#    /root/.jupyter
#    /venv/etc/jupyter
#    /usr/local/etc/jupyter
#    /etc/jupyter
#data:
#    /root/.local/share/jupyter
#    /venv/share/jupyter
#    /usr/local/share/jupyter
#    /usr/share/jupyter
#runtime:
#    /root/.local/share/jupyter/runtime
#
#
# dev:
#   docker build -t amc
#   docker run -t amc

FROM python:3.8

USER root
RUN apt-get update
RUN apt-get install -y tree
# needed to build pyzmq in 3.8
RUN apt-get install -y libzmq3-dev

# https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
ARG NB_USER=ob
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

USER ${NB_USER}
ENV VIRTUAL_ENV=${HOME}/venv
RUN python3.8 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install cython
RUN pip install --no-cache-dir jupyter==1.0.0 rise==5.5.1 pytest==5.1.2

WORKDIR ${HOME}
COPY . ${HOME}

USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

ENV HOME_IPYTHON_PROFILE=$HOME/.ipython/profile_default
RUN mkdir -p $HOME_IPYTHON_PROFILE/startup
# TODO I might need this
# RUN cp __customized__/jupyter_notebook_config.py $HOME_IPYTHON_PROFILE/jupyter_notebook_config.py
RUN cp __customized__/99-amc-ipython-startup.py $HOME_IPYTHON_PROFILE/startup/99-amc-ipython-startup.py

ENV VENV_JUPYTER_NBCONFIG=$VIRTUAL_ENV/etc/jupyter/nbconfig
RUN mkdir -p $VENV_JUPYTER_NBCONFIG
RUN cp __customized__/rise.json $VENV_JUPYTER_NBCONFIG/rise.json
RUN jupyter-nbextension install rise --py --sys-prefix
RUN jupyter-nbextension enable rise --py --sys-prefix

RUN jupyter --version
RUN jupyter --paths
