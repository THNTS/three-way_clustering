from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotVisibleException, ElementNotInteractableException
from selenium import webdriver
import time
import pandas as pd
from Scraper import get_jobs
import os
import multiprocessing
from itertools import product


if __name__ == '__main__':
    job_positions = ["Cloud System Engineer", "IT Coordinator", "Help Desk Technician",
                     "Data Quality Manager", "Applications Engineer", "Web Administrator",
                     "Management Information Systems Director", "IT director", "Data scientist",
                     "IT security specialist", "Software engineer", "Computer scientist",
                     "Database administrator", "User experience designer",  "Network engineer",
                     "System analyst", "IT technician", "Web developer", "Quality assurance tester",
                     "Computer programmer", "Support specialist"]
    cities = ["San Francisco", "London"]
    results = []
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.starmap(get_jobs, product([
                     "Network engineer",
                     "System analyst", "Quality assurance tester",
                     "Computer programmer"],
                                                 ["London"], [300]))
    result=get_jobs("IT Coordinator", "San Francisco", 300)