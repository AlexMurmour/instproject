import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import conf
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import sys


webdriver = webdriver.Firefox()
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys(conf.username)
password = webdriver.find_element_by_name('password')
password.send_keys(conf.password)

button_login = webdriver.find_element_by_css_selector(
    '#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(3) > button')
button_login.click()
sleep(3)

notnow = webdriver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[3]/button[2]')
notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications

hashtag_list = ['travelblog', 'travelblogger', 'traveler']

prev_user_list = [] #if it's the first time you run it, use this line and comment the two below
# prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,
#                  1:2]  # useful to build a user log
# prev_user_list = list(prev_user_list['0'])

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0
pic_hrefs = []

for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(5)

    for i in range(1, 7):
        try:
            webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            # get tags
            hrefs_in_view = webdriver.find_elements_by_tag_name('a')
            # finding relevant hrefs
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                             if '.com/p/' in elem.get_attribute('href')]
            # building list of unique photos
            [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
            # print("Check: pic href length " + str(len(pic_hrefs)))
        except Exception:
            continue

    for pic_href in pic_hrefs:
        webdriver.get(pic_href)
        sleep(2)
        username= webdriver.find_element_by_tag_name('h2').text
        if username not in prev_user_list:
        # If we already follow, do not unfollow
            if followed < 50:
                if webdriver.find_element_by_xpath(
                        '//span[@button="Подписаться"]').text == 'Подписаться':

                    webdriver.find_element_by_xpath(
                        '//span[@button="Подписаться"]').click()

                    new_followed.append(username)
                    followed += 1

                    # Liking the picture
            if likes < 100:
                button_like = webdriver.find_element_by_xpath(
                            '//span[@aria-label="Нравится"]')

                button_like.click()
                likes += 1
                sleep(randint(18, 25))

                # Comments and tracker
            if comments < 50:
                comm_prob = randint(1, 10)
                print('{}: {}'.format(hashtag, comm_prob))
                if comm_prob > 7:
                    comments += 1
                    webdriver.find_element_by_xpath(
                        '/html/body/div[3]/div/div[2]/div/article/div[2]/section[3]/div/form/textarea').click()
                    comment_box = webdriver.find_element_by_xpath(
                        '/html/body/div[3]/div/div[2]/div/article/div[2]/section[3]/div/form/textarea')

                    if (comm_prob < 7):
                        comment_box.send_keys('Really cool!')
                        sleep(1)
                    elif (comm_prob > 6) and (comm_prob < 9):
                        comment_box.send_keys('Nice work :)')
                        sleep(1)
                    elif comm_prob == 9:
                        comment_box.send_keys('Nice gallery!!')
                        sleep(1)
                    elif comm_prob == 10:
                        comment_box.send_keys('So cool! :)')
                        sleep(1)
                    # Enter to post comment
                    comment_box.send_keys(Keys.ENTER)
                    sleep(randint(22, 28))

                # Next picture

                sleep(randint(25, 29))


    # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next


for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
# def print_same_line(text):
#     sys.stdout.write('\r')
#     sys.stdout.flush()
#     sys.stdout.write(text)
#     sys.stdout.flush() # Отражает процесс выполнения
#
#
# class InstagramBot:
#
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.driver = webdriver.Firefox()
#
#     def closeBrowser(self):
#         self.driver.close()
#
#     def login(self):
#         driver = self.driver
#         driver.get("https://www.instagram.com/")
#         time.sleep(2)
#         login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
#         login_button.click()
#         time.sleep(2)
#         user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
#         user_name_elem.clear()
#         user_name_elem.send_keys(self.username)
#         passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
#         passworword_elem.clear()
#         passworword_elem.send_keys(self.password)
#         passworword_elem.send_keys(Keys.RETURN)
#         time.sleep(2)
#
#
#     def like_photo(self, hashtag):
#         driver = self.driver
#         driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
#         time.sleep(2)
#
#         # gathering photos
#         pic_hrefs = []
#         for i in range(1, 7):
#             try:
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(2)
#                 # get tags
#                 hrefs_in_view = driver.find_elements_by_tag_name('a') #
#                 # finding relevant hrefs
#                 hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
#                                  if '.com/p/' in elem.get_attribute('href')]
#                 # building list of unique photos
#                 [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
#                 # print("Check: pic href length " + str(len(pic_hrefs)))
#             except Exception:
#                 continue
#
#         # Liking photos
#         unique_photos = len(pic_hrefs)
#         for pic_href in pic_hrefs:
#             driver.get(pic_href)
#             time.sleep(2)
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             try:
#                 time.sleep(random.randint(2, 4))
#                 like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Нравится"]').click()
#                 like_button().click()
#                 for second in reversed(range(0, random.randint(18, 28))):
#                     print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
#                                     + " | Sleeping " + str(second))
#                     time.sleep(1)
#             except Exception as e:
#                 time.sleep(2)
#             unique_photos -= 1
#
#
#
# username = conf.username
# password = conf.password
#
# ig = InstagramBot(username, password)
# ig.login()
#
# hashtags = ['amazing', 'beautiful', 'adventure', 'photography', 'nofilter',
#             'newyork', 'artsy', 'alumni', 'lion', 'best', 'fun', 'happy',
#             'art', 'funny', 'me', 'followme', 'follow', 'cinematography', 'cinema',
#             'love', 'instagood', 'instagood', 'followme', 'fashion', 'sun', 'scruffy',
#             'street', 'canon', 'beauty', 'studio', 'pretty', 'vintage', 'fierce']
#
# while True:
#     try:
#         # Choose a random tag from the list of tags
#         tag = random.choice(hashtags)
#         ig.like_photo(tag)
#     except Exception:
#         ig.closeBrowser()
#         time.sleep(60)
#         ig = InstagramBot(username, password)
#         ig.login()