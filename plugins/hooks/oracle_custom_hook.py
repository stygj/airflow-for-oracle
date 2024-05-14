from contextlib import contextmanager
from typing import Optional, Generator
import oracledb
from airflow.hooks.base import BaseHook


class OracleCustomHook(BaseHook):
    def __init__(self, user: str, password: str, dsn: str) -> None:
        self.user: str = user
        self.password: str = password
        self.dsn: str = dsn
        
    @contextmanager
    def get_conn(self) -> Generator[oracledb.Connection, None, None]:
        conn: Optional[oracledb.Connection] = None
        try:
            oracledb.init_oracle_client(lib_dir="/usr/lib/oracle/11.2/client64/lib")
            conn = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
                )
            yield conn
        finally:
            if conn:
                conn.close()
