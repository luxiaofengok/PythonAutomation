import pytest
from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class TestSearchWiki:
    def read_data_from_file(file_path):
        with open(file_path, mode='r') as file:
            csv_reader=csv.DictReader(file)
            keywords=[]
            for row in csv_reader:
                keywords.append(row['keyword'])
            return keywords
        
    testdata= read_data_from_file("data.csv")
    
    @pytest.mark.parametrize("keyword", testdata)
    def test_search_wikipedia(self, driver, keyword):
        search_box=driver.find_element(By.NAME, "search")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        sleep(5)