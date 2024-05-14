## Airflow for oracle
Oracle 11g와 같은 레거시 환경에서 AWS Athena를 활용한 분석용 데이터를  추출 하기 위해 만든 Airflow Repository 입니다.

## 디렉토리 구조
~~~
.
├── README.md
├── .gitignore
├── airflow.cfg
├── docker-compose.yml
├── Dockerfile
├── requirements.tzt
├── dags
│   ├── __init__.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── s3_connect.py
│   ├── dag_example.py
│   ├── ...
├── oracle_bins
│   ├── oracle-instantclient11.2-basic_11.2.0.4.0-1_amd64.deb
│   ├── oracle-instantclient11.2-sqlplus_11.2.0.4.0-1_amd64.deb
├── plugins
│   ├── __init__.py
│   ├── hooks
│   │   ├── __init__.py
│   │   ├── athena_custom_hook.py
│   │   ├── oracle_custom_hook.py
~~~

## Admin Variable List
~~~
- PROD_DB_PASSWORD : 운영 DB Password
- PROD_DB_USER : 운영 DB User
- PROD_DB_DSN : 운영 DB DSN ex) localhost:1521:XE
- S3_ACCESS_KEY_ID : AWS Key Id
- S3_SECRET_KEY : AWS key
- S3_BUCKET : S3 버킷 이름
~~~