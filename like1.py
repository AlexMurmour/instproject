from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep  
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
import conf

follows = 0
likes = 0
comments = 0
pic_hrefs = []

hashtags = ['beauty', 'naruto', 'sailormoon']
driver = webdriver.Firefox()

def login():
    sleep(2)
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)

    username = driver.find_element_by_name('username')
    username.send_keys(conf.username)
    password = driver.find_element_by_name('password')
    password.send_keys(conf.password)
    password.send_keys(Keys.RETURN)
    sleep(3)

    notnow = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "aOOlW.HoLwm")))
    notnow.click()


def create_pic_list():
    for hashtag in hashtags:
        driver.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
        sleep(2)
        global pic_hrefs
        for i in range(1, 30):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding hrefs
                hrefs_in_view = [unit.get_attribute('href') for unit in hrefs_in_view
                                 if '.com/p/' in unit.get_attribute('href')]
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
                sleep(2)
            except Exception:
                continue
    return pic_hrefs


def like():
    global likes
    sleep(randint(2, 4))
    driver.find_element_by_xpath('//span[@aria-label="Нравится"]').click()
    sleep(1)
    likes += 1
    return likes


def follow(user):
    global follows
    case = randint(1, 10)
    if case > 5:
        driver.find_element_by_xpath(
            "//button[contains(text(), 'Подписаться')]").click()
        sleep(1)
        open('users.txt', 'a').write(", " + user)
        follows += 1
        print('добавлен ' + user)  # user make str not int
    if case < 5:
        sleep(1)
    return follows



def comment():
    global comments
    comm = randint(1, 10)
    if comm > 7:
        driver.find_element_by_xpath('//textarea[@placeholder = "Добавьте комментарий..."]').click()
        comment_box = driver.find_element_by_xpath(
            '//textarea[@placeholder = "Добавьте комментарий..."]')

        if (comm < 7):
            comment_box.send_keys('Really cool!')
            sleep(1)
        elif (comm > 6) and (comm < 9):
            comment_box.send_keys('Nice work :)')
            sleep(1)
        elif comm == 9:
            comment_box.send_keys('Nice gallery!!')
            sleep(1)
        elif comm == 10:
            comment_box.send_keys('So cool! :)')
            sleep(1)
        # Enter to post comment
        comment_box.send_keys(Keys.ENTER)
        comments += 1
        sleep(randint(22, 28))
    return comments


def main():
    login()
    create_pic_list()
    for href in pic_hrefs:
        try:
            driver.get(href)
            sleep(3)
            user = driver.find_element_by_tag_name('h2').text
            print(user)
            if user in open('users.txt'):
                pass
            elif user not in open('users.txt'):
                if likes < 700:
                    like()
                if follows < 50:
                    follow(user)
                    print('follows: ' + str(follows))
                if comments < 80:
                    comment()
                    print('comments: ' + str(comments))
        except Exception as e:
            print(e)
            sleep(2)
    print(likes, follows, comments)


if __name__ == "__main__":
    main()

