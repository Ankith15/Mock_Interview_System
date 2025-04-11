# This is the common file for functions
import speech_recognition as sr
import os
import pyttsx3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

class Text2Speech:
    engine: pyttsx3.Engine

    def __init__(self,voice,rate:int,volume:float):
        self.engine = pyttsx3.init()
        if voice:
            self.engine.setProperty("voice",voice)
            self.engine.setProperty('rate',rate)
            self.engine.setProperty('volume',volume)

    def list_available_voices(self):
        voices: list =[self.engine.getProperty('voices')]

        for i, voice in enumerate(voices[0]):
            print(f"{i+1} {voice.name} {voice.age}: {voice.languages} ({voice.gender}) [{voice.id}]")

    def text_to_speech(self, text:str,save:bool = False,file_name = "output.mp3"):
        
        self.engine.say(text)
        print('I am speaking')
        
        if save:
            self.engine.save_to_file(text,file_name)

        self.engine.runAndWait()


class Speech2Text:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic= sr.Microphone()

    def live_speech_to_text(self):
        print("Start Answering the question")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.audio_data=[]
            last_speech_time = time.time()
            self.silence_threshold = 3

            while True:
                try:
                    self.audio = self.recognizer.listen(source,timeout = self.silence_threshold,phrase_time_limit = 10)
                    self.audio_data.append(self.audio)
                    last_speech_time = time.time()
                
                except sr.WaitTimeoutError:
                    print("Your answer has been recorded")
                    break
                except Exception as e:
                    print(f"Error for the given is {e}")
                    break

        if self.audio_data:
            full_audio = sr.AudioData(b"".join([a.get_raw_data() for a in self.audio_data]),
            sample_rate = self.audio_data[0].sample_rate,
            sample_width = self.audio_data[0].sample_width)

            try:
                text = self.recognizer.recognize_google(full_audio)
                print("Transcription:",text)
                return text

            except sr.UnknownValueError:
                print("Could not understand the audio.")

            except sr.RequestError:
                print("Error connecting to Google API")

        else:
            print("No speech recorded.")

#Scrapping Naukri

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

        self.driver.quit()