from src.apies.hh.configs import ACCESS_TOKEN as HH_ACCESS_TOKEN, USER_AGENT as HH_USER_AGENT
from src.apies.hh.HHDataCollector import HHDataCollector


def create_data_collector():
    return HHDataCollector(HH_ACCESS_TOKEN, HH_USER_AGENT)

