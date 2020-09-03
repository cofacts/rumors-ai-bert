FROM tiangolo/meinheld-gunicorn-flask:python3.7
RUN mkdir /app/tasks
#RUN mkdir /root/.ssh
#Run touch /root/.ssh/google_compute_engine
#WORKDIR /app
RUN mkdir /root/run-scripts
RUN mkdir /root/run-scripts/tasks
WORKDIR /root/run-scripts

#COPY ./task_handler.py /app/
#COPY ./config.py /app/
#COPY ./transform_json_to_csv.py /app/

#COPY ./start_GPU.sh /app/
#COPY ./stop_GPU.sh /app/
#COPY ./send_task.sh /app/

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
#ENTRYPOINT python /main.py
#ENTRYPOINT ["bash"]
## directly curl
##ENTRYPOINT python

#RUN ls -a
#CMD python /app/task_handler.py
CMD python /root/run-scripts/task_handler2.py
#CMD bash
