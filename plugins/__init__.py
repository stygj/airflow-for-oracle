from typing import List
from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base import BaseHook
from hooks.oracle_custom_hook import OracleCustomHook
from hooks.athena_custom_hook import AthenaCustomHook


class CustomHookPlugin(AirflowPlugin):
    name: str = 'custom_hook'
    hooks: List[BaseHook] = [OracleCustomHook, AthenaCustomHook] 
