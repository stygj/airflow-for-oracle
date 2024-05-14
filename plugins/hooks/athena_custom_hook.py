from contextlib import contextmanager
from typing import Optional, Generator, Callable
import pyathena
from airflow.hooks.base import BaseHook


class AthenaCustomHook(BaseHook):
    def __init__(self,
                 bucket_path: str,
                 region_name: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str
                 ) -> None:
        self.bucket_path: str = bucket_path
        self.region_name: str = region_name
        self.aws_access_key_id: str = aws_access_key_id
        self.aws_secret_access_key: str = aws_secret_access_key
    
    @contextmanager
    def get_conn(self) -> Generator[Callable, None, None]:
        conn: Optional[Callable] = None
        try:
            conn = pyathena.connect(
                s3_staging_dir=self.bucket_path,
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )
            yield conn
        finally:
            if conn:
                conn.close()
