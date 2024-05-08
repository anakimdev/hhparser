from src.apies.hh.configs import ACCESS_TOKEN as HH_ACCESS_TOKEN, USER_AGENT as HH_USER_AGENT, BASE_URL as HH_BASE_URL
from src.apies.hh.HHDataCollector import HHDataCollector
from src.apies.company_info.InnDataCollector import  InnDataCollector
from src.apies.company_info.CompanyDataCollector import CompanyDataCollector


def create_hunter_collector():
    return HHDataCollector(HH_ACCESS_TOKEN, HH_USER_AGENT, HH_BASE_URL)


def create_inn_collector():
    return InnDataCollector()


def create_company_collector():
    return CompanyDataCollector()