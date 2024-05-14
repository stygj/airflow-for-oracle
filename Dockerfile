FROM apache/airflow:slim-2.8.3-python3.11

USER root
# oracle 관련 패키지 설치
RUN apt-get update
RUN apt-get install -y libaio1
RUN apt-get install -y dpkg-dev
RUN mkdir -p /oracle_bins
COPY oracle_bins/. /oracle_bins/
WORKDIR /oracle_bins
RUN dpkg -i oracle-instantclient11.2-basic_11.2.0.4.0-1_amd64.deb
RUN dpkg -i oracle-instantclient11.2-sqlplus_11.2.0.4.0-1_amd64.deb

USER airflow
WORKDIR /opt/airflow
# # 필요 dependency 설치
COPY requirements.txt /opt/airflow/
RUN pip install --no-cache-dir -r requirements.txt

# 데이터를 적재할 폴더 생성
RUN mkdir -p /opt/airflow/data

# airflow.cfg 복사
COPY airflow.cfg /opt/airflow/

