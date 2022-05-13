from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import date, datetime
import pandas as pd
import pymssql
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

conn=pymssql.connect(server='192.168.10.216', user='sa', password='123', database='MAS')
cursor = conn.cursor(as_dict=True)

url = 'https://www.boursorama.com/bourse/devises/cours/historique/1xEURMAD?fromSymbol=EUR&toSymbol=MAD&fromLabel=euro&toLabel=dirham&fbclid=IwAR1uOKsnToQabmU8nOz29IkMMA9-sGG3UAid4kQ8XsiJSwS306euTEiprpA'
urlUSD = 'https://www.boursorama.com/bourse/devises/cours/historique/3fUSD_MAD?fromSymbol=USD&toSymbol=MAD&fromLabel=dollar&toLabel=dirham'
driver.get(url)


btnCookies = driver.find_element_by_class_name('didomi-continue-without-agreeing')
btnCookies.click()
dt = driver.find_element_by_id('historic_search_startDate')
dt.click()
button = driver.find_element_by_id('historic_search_filter')
currentTimeDate = datetime. now()

dd = str(date.today()).split("-")
dt.clear()
dt.send_keys(dd[2]+"-"+dd[1]+"-"+dd[0])
dt.send_keys(Keys.TAB)
button.click()
time.sleep(2)
df = pd.read_html(driver.page_source)[0]
del df["Var. %"]
del df["+ haut"]
del df["+ bas"]
del df["Ouverture"]
req1 = f"insert into polycoffre..coursdevise (CoursDevise, CoursAchat, CoursVente, CoursDate, CoursBanque) values ('EUR', {df['Dernier'][0]}, {df['Dernier'][0]}, {dd[2]+'-'+dd[1]+'-'+dd[0]}, 'BCM')"


driver.get(urlUSD)

dt = driver.find_element_by_id('historic_search_startDate')
dt.click()
button = driver.find_element_by_id('historic_search_filter')
currentTimeDate = datetime. now()

dd = str(date.today()).split("-")
dt.clear()
dt.send_keys(dd[2]+"-"+dd[1]+"-"+dd[0])
dt.send_keys(Keys.TAB)
button.click()
time.sleep(2)
df1 = pd.read_html(driver.page_source)[0]
del df1["Var. %"]
del df1["+ haut"]
del df1["+ bas"]
del df1["Ouverture"]
req2 = f"insert into polycoffre..coursdevise (CoursDevise, CoursAchat, CoursVente, CoursDate, CoursBanque) values ('USD', {df1['Dernier'][0]}, {df1['Dernier'][0]}, {dd[2]+'-'+dd[1]+'-'+dd[0]}, 'BCM')"

# cursor.execute(req1)
# cursor.execute(req2)
print(req1)
print(req2)

