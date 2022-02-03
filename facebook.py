#!/usr/bin/env python
# coding: utf-8

# In[103]:

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time


# In[104]:
user_name=""
user_password=""
keyword=""
error_message="veuillez entrer la requete sous forme de 'python facebook.py \"Email de l'utilisateur\" \"mot de passe de compte\" \"le sujet que vous cherchez \" ' "
try:
    user_name = sys.argv[1]
except:
    sys.stdout.write(error_message)
    sys.stdout.write("veuillez entrer votre nom d'utilisateur")
    sys.exit()
try:
    user_password = sys.argv[2]
except:
    sys.stdout.write(error_message)
    sys.stdout.write("vieullez entrer votre mot de passe")
    sys.exit()
try:
    keyword = sys.argv[3]
except:
    sys.stdout.write(error_message)
    sys.stdout.write("vieullez entrer le sujet recherche")
    sys.exit()


chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
user_password="a18031996a"
#il faut telecharger le fichier chromedriver.exe et maitre son chemin comme premier argument dans la fonction de webdriver.chrome
 
driver = webdriver.Chrome('C:/Users/Client/Documents/cours/AIC/chromedriver.exe',chrome_options=chrome_options)
driver.get("http://www.facebook.com") #ouvrir le navigateur et le rediriger vers la page de facebook.com
time.sleep(5)
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Tout accepter']"))).click()
time.sleep(5)



# In[105]:


username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

#entrer l'email et le mot de passe
username.clear()
username.send_keys(user_name)
password.clear()
password.send_keys(user_password)

#pour cliquer sur connecter 
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
#connecter à un compte Facebook
time.sleep(10)
# In[106]:



searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Rechercher sur Facebook']")))
searchbox.clear()

searchbox.send_keys(keyword)
#entrer la requete dans la bar de recherche de Facebook

time.sleep(5)
searchbox.send_keys(Keys.ENTER)
time.sleep(5)
searchbox.send_keys(Keys.ENTER)
time.sleep(5)


# In[107]:


import re
link = driver.current_url
new_link = re.sub(r'top', 'posts', link)
#afficher les publication liees au sujet recherche

# In[108]:


driver.get(new_link)
time.sleep(10)

# In[109]:


import pymongo
url='mongodb://127.0.0.1:27017/'
con  = pymongo.MongoClient(url)
mydb=con['scrapper']
pub = mydb['publications']

#se connecter a la base de donnees
# In[111]:


all_publications = driver.find_elements(By.CSS_SELECTOR,'body > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div > div > div ')
#selectioner que les div qui contiennent des publications
for publication in all_publications:
    post={}
    try:
        post['texte']=publication.find_elements(By.CSS_SELECTOR,'div[dir="auto"]')[0].get_attribute('innerText')
        #selectioner le texte de la publication
    except:
        pass
    try:
        post['image']=publication.find_elements(By.CSS_SELECTOR,'div[dir="auto"]+div')[0].find_elements_by_tag_name('img')[0].get_attribute('src')
        #selectioner le l'image de la publication
    except:
        pass
    if post != {}:
        pub.insert_one(post)
        #inserer la publication dans la base de donnees

# In[ ]:




