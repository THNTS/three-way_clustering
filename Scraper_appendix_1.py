from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,\
    ElementNotVisibleException, ElementNotInteractableException, StaleElementReferenceException, TimeoutException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_jobs(keyword, city, num_jobs, verbose=False):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.FirefoxOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path="/Users/daniilbabin/DS/geckodriver", options=options)
    driver.set_window_size(1120, 1000)

    cities_dict = {
        'San Francisco': '1147401',
        'London': '2671300'
    }

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + keyword + '&locT=C&locId=' + cities_dict[city] + '&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(2)

        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(2)

        #         driver.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/div[2]/div/div/div[3]/button').click()
        #         time.sleep(3)
        try:
            driver.find_element_by_xpath("//*[name()='path' and contains(@id,'prefix__icon-close-1')]").click()
        except NoSuchElementException:
            pass
        time.sleep(2)
        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("jl")  # jl for Job Listing. These are the buttons we're going to click.

        #         //Now after all your stuff done inside frame need to switch to default content
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            try:
                job_button.click()  # You might
            except ElementNotInteractableException:
                continue
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(3)

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:

                WebDriverWait(driver, 10).until(
                    expected_conditions.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/section/div/div/article/div/div[2]/div[1]/div[1]/div/div/div[2]/span')))
                driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/div/div[2]/section/div/div/article/div/div[2]/div[1]/div[1]/div/div/div[2]/span').click()
                time.sleep(2)

                try:
                    # <div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    # </div>
                    headquarters = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1
            except StaleElementReferenceException:
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1
            except TimeoutException:
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1
            except ElementClickInterceptedException:
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1
            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})
            # add job to jobs
        # Clicking on the "next page" button
        try:
            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located((By.XPATH, './/li[@class="next"]//a')))
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            time.sleep(2)
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break

    df = pd.DataFrame(jobs)
    df.insert(0, "Position", keyword)
    df.insert(1, "City", city)
    df.to_csv(keyword + "_" + city + ".csv")
    driver.quit()

    return 0
