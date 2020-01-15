import time

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# TODO - set optimal time and epicenter from there without explicit times
acceptable_times = [
	'7:30PM',
	'7:15PM',
	'7:45PM',
	'7:00PM',
	'8:00PM',
	'6:45PM',
	'8:15PM',
	'6:30PM',
	'8:30PM',
	'6:15PM',
	'8:45PM',
	'9:00PM',
	'9:15PM',
	'9:30PM',
	'6:00PM',
	'9:45PM',
	'10:00PM',
	'10:15PM',
	'10:30PM',
	'10:45PM',
	'11:00PM',
]

# kick off prior to midnight

driver = webdriver.Chrome()
driver.get("https://resy.com/cities/ny/rezdora")  # assuming we don't get redirected
# TODO assert requested date is still in url (not redirected)

# clear announcement if present
driver.implicitly_wait(3)
announcement_btn = driver.find_element_by_class_name("AnnouncementModal__icon-close")
if announcement_btn:
	announcement_btn.click()

# login
login_btn = driver.find_element_by_xpath("//resy-menu-container/div/div/button")
login_btn.click()
time.sleep(1)
alt_auth_btn = driver.find_element_by_xpath("//div[contains(@class, 'AuthView__Footer')]/button")
alt_auth_btn.click()
time.sleep(1)
login_form_identifier = "//form[@name='login_form']/div"
email_input = driver.find_element_by_xpath(login_form_identifier + "/input[@name='email']")
email_input.send_keys('********')
password_input = driver.find_element_by_xpath(login_form_identifier + "/input[@name='password']")
password_input.send_keys('********')
password_input.send_keys(Keys.RETURN)

while datetime.now() < datetime(2020, 1, 15):
	print('waiting for midnight...')
	time.sleep(2)

driver.get("https://resy.com/cities/ny/rezdora?date=2020-02-13&seats=2")

# find a time
time.sleep(1)
driver.implicitly_wait(0)
available_time = None
base_time_prefix = "//resy-reservation-button//div[contains(@class, 'time') and contains(text(), '"
for acceptable_time in acceptable_times:
	try:
		xpath_q = base_time_prefix + acceptable_time + "')]"
		available_time = driver.find_element_by_xpath(xpath_q)
		break
	except NoSuchElementException:
		continue

if not available_time:
	# driver.close()
	exit('no acceptable_times available')

driver.implicitly_wait(3)
# book reservation
available_time.click()
time.sleep(3)
iframe = driver.find_elements_by_tag_name('iframe')[0]
driver.switch_to.frame(iframe)
confirm_btn = driver.find_element_by_xpath("//button[@class='button primary']")
time.sleep(1)
confirm_btn.click()

# done
# driver.close()
