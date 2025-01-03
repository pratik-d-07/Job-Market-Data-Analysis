from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver options

service = Service("D:\Web Mining Project New\chromedriver-win64\chromedriver.exe") 

# Launching the browser
driver = webdriver.Chrome(service=service,)

# Navigate to Naukri.com
url = "https://www.naukri.com/software-developer-jobs?k=software%20developer&nignbevent_src=jobsearchDeskGNB"
driver.get(url)
time.sleep(5)  # Wait for page to load

# Function to close any popup that appears
def close_popup():
    try:
        close_button = driver.find_element(By.XPATH, '//a[@id="login_Layer"]')
        close_button.click()
        time.sleep(2)
    except NoSuchElementException:
        pass

# Job limit for scraping
job_limit = 20

# Initialize a list to hold job data
job_data = []

# Track the number of jobs scraped
scraped_jobs = 0

# Loop through pages until the job limit is reached
while scraped_jobs < job_limit:

    # Parse the current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = soup.find_all('div', class_='srp-jobtuple-wrapper')

    # Extract data from each job card on the current page
    for job in jobs:
        if scraped_jobs >= job_limit:
            break  # Stop if we reach the job limit

        # Initialize a dictionary for job information
        job_info = {
            "Job Title": None,
            "Company Name": None,
            "Rating": None,
            "Experience": None,
            "Salary": None,
            "Location": None,
            "Skills": None
        }

        # Populate the dictionary with job information
        title = job.find('a', class_='title')
        job_info["Job Title"] = title.text.strip() if title else None

        company = job.find('a', class_='comp-name')
        job_info["Company Name"] = company.text.strip() if company else None

        rating = job.find('span', class_='main-2')
        job_info["Rating"] = rating.text.strip() if rating else None

        experience = job.find('span', class_='expwdth')
        job_info["Experience"] = experience.text.strip() if experience else None

        salary_outer = job.find('span', class_='sal')
        job_info["Salary"] = salary_outer.find('span').text.strip() if salary_outer and salary_outer.find('span') else None

        location = job.find('span', class_='locWdth')
        job_info["Location"] = location.text.strip() if location else None

        skill_list = job.find('ul', class_='tags-gt')
        skills = [skill.text.strip() for skill in skill_list.find_all('li', class_='dot-gt')[:5]] if skill_list else []
        job_info["Skills"] = ", ".join(skills)

        # Append job_info to job_data
        job_data.append(job_info)
        scraped_jobs += 1

    # Try to go to the next page if more jobs are needed
    if scraped_jobs < job_limit:
        try:
            next_button = driver.find_element(By.XPATH, '//a[@class="styles_btn-secondary__2AsIP"]')
            driver.execute_script("arguments[0].scrollIntoView();", next_button)  # Scroll to "Next" button
            driver.execute_script("arguments[0].click();", next_button)  # Click with JavaScript
            time.sleep(5)  # Wait for the next page to load
        except NoSuchElementException:
            print("No more pages found.")
            break
        except ElementClickInterceptedException:
            print("Next button was intercepted. Trying to close popups.")
            close_popup()
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)

# Convert list of job data to DataFrame
job_df = pd.DataFrame(job_data)

# Close the browser
driver.quit()

# Display or save the data
job_df.to_csv('naukri_jobs_test.csv', index=False)
print("Saved successfully to naukri_jobs.csv")