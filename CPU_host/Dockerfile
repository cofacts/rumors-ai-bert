FROM tiangolo/meinheld-gunicorn-flask:python3.7
RUN mkdir /app/tasks

RUN mkdir /root/run-scripts
RUN mkdir /root/run-scripts/tasks
WORKDIR /root/run-scripts


COPY ./Pipfile /root/run-scripts/
COPY ./Pipfile.lock /root/run-scripts/
RUN  pip install pipenv && pipenv install --deploy --dev --system

RUN apt-get update && apt-get -y install sudo

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN sudo apt-get install apt-transport-https ca-certificates gnupg -y
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
#RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
RUN sudo apt-get update && sudo apt-get install google-cloud-sdk -y

ENV FLASK_APP=/main.py

CMD python /root/run-scripts/task_handler.py --debug_mode True --category_num 17
