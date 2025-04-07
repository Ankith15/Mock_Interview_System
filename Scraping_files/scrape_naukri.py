import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

class JobAgent:
    def __init__(self, job_role, location, experience, freshness):
        self.job_role = job_role
        self.location = location
        self.experience = experience
        self.freshness = freshness
        self.service = Service(os.getenv("EDGE_DRIVER_PATH", "msedgedriver.exe"))
        self.driver = webdriver.Edge(service=self.service)
        self.current_url = None

    def url_naukri(self):
        """Navigates to Naukri and performs job search."""
        self.driver.get("https://www.naukri.com")
        wait = WebDriverWait(self.driver, 15)

        # Select job role input field
        role_input = self.driver.find_element(By.CLASS_NAME, "suggestor-input")
        role_input.send_keys(self.job_role)
        time.sleep(1)
        role_input.send_keys(Keys.DOWN)
        time.sleep(1)
        role_input.send_keys(Keys.ENTER)
        time.sleep(3)

        # Select location input field
        location = self.driver.find_element(By.CSS_SELECTOR, ".locationSugg input")
        location.send_keys(self.location)
        time.sleep(1)
        location.send_keys(Keys.DOWN)
        time.sleep(1)
        location.send_keys(Keys.ENTER)

        # Click on the search button
        submit = self.driver.find_element(By.CSS_SELECTOR, ".qsbSubmit")  
        submit.click()
        time.sleep(5)
        
        # Store current URL
        self.current_url = self.driver.current_url
        print(f"Captured URL: {self.current_url}")

    def scrapper(self):
        """Extracts job postings from the search results page."""
        
        url = f"{self.current_url}&experience={self.experience}&jobAge={self.freshness}"
        print("Navigating to:", url)
        
        self.driver.get(url)
        jobi = []
        wait = WebDriverWait(self.driver, 15)

        col = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "listContainer")))
        job_elements = col.find_elements(By.CLASS_NAME, "cust-job-tuple")  # Extract all job listings

        jobs = []
        company = []
        experience=[]
        salary = []
        location = []
        # description=[]
        skills=[]
        posted=[]
        ml=[]
        temp=[]
        for i in job_elements:
            ml.append([i])
            
        for i in range(len(ml)):
            for j in ml[i]:
                temp.append(j)
        for i in range(len(temp)):
            jobs.append(temp[i].text.split("\n")[0])
            company.append(temp[i].text.split("\n")[1])
            experience.append(temp[i].text.split("\n")[4])
            salary.append(temp[i].text.split("\n")[5])
            skills.append(temp[i].text.split("\n")[-3])
            posted.append(temp[i].text.split("\n")[-2])

            
        
        
        print(jobs)
        print(company)
        print(experience)
        print(salary)
        print(location)
        print(skills)
        print(posted)

       

        # Close the browser
        self.driver.quit()


if __name__ == "__main__":
    agent = JobAgent("Data Analyst", "Bangalore", 2, 7)
    agent.url_naukri()  # Fetch the search URL
    agent.scrapper()    # Scrape jobs
