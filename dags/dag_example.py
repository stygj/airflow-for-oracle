from datetime import datetime
from textwrap import dedent
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator


def extract_product():
    import csv
    from airflow.models.variable import Variable
    from hooks.oracle_custom_hook import OracleCustomHook
    
    query = f"""
        SELECT quantity, price
        FROM product
    """
    with OracleCustomHook(
            user=Variable.get("PROD_DB_USER"),
            password=Variable.get("PROD_DB_PASSWORD"),
            dsn=Variable.get("PROD_DB_DSN")
        ).get_conn() as conn:
        cursor = conn.cursor()
        cursor.arraysize = 5000
        cursor.execute(query)
        
        with open("/opt/airflow/data/product.csv", "w", encoding="utf-8") as f:
            writer = csv.writer(
                    f,
                    delimiter=",",
                    lineterminator="\n"
                    )
            writer.writerow([row[0] for row in cursor.description])
            while True:
                data = cursor.fetchmany()
                if not data: 
                    break
                for row in data:
                    writer.writerow(row)
        
        cursor.close()


def load_to_s3():
    import datetime
    from airflow.models.variable import Variable
    from utils.s3_connect import S3Client
    from hooks.athena_custom_hook import AthenaCustomHook
    
    now = datetime.datetime.now()
    S3Client().upload_file(
        "/opt/airflow/data/product.csv",
        f"MY_BUCKET/product/year={now.year}/month={now.month}/product_{now}.csv"
    )
    with AthenaCustomHook(
            bucket_path=f"s3://MY_BUCKET/", 
            region_name="ap-northeast-2",
            aws_access_key_id=Variable.get('S3_ACCESS_KEY_ID'),
            aws_secret_access_key=Variable.get('S3_SECRET_KEY')
        ).get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("msck repair table my_bucket.product")


with DAG(
    dag_id="oracle_to_athena",
    description="copy Oracle product data to AWS Athena",
    start_date=datetime(2024,3,18),
    schedule_interval="50 23 * * *"
) as dag:
    dag.doc_md = __doc__
    dag.doc_md = """
        오라클에서 관리중인 상품 데이터를 추출하여 AWS Athena에서 조회하기 위한 DAG
    """
    task1 = PythonVirtualenvOperator(
        task_id="extract_product",
        python_callable=extract_product,
        requirements=["oracledb"],
        python_version='3.11'
    )
    task1.doc_md = dedent(
        """
        Oracle DB에서 상품 데이터를 추출
        """
    )
    
    task2 = PythonVirtualenvOperator(
        task_id="load_to_s3",
        python_callable=load_to_s3,
        requirements=["boto3", "pyathena"],
        python_version='3.11'
    )
    task2.doc_md = dedent(
        """
        추춝된 상품을 S3에 업로드
        """
    )

    task1 >> task2