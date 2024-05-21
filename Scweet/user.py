from . import utils
from time import sleep
import random
import json
import pandas as pd
import datetime
import csv

def get_user_information(users, driver=None, headless=True):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless)
    date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'outputs/{date_str}_user.csv'
    header = ['additionalName', 'givenName', 'image', 'background_image', 'following', 'followers', 'tweet_num', 'type', 'join_date', 'description', 'website']
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
               
    for i, user in enumerate(users):

        log_user_page(user, driver)

        if user is None:
            print('You must specify a user.')
            continue

        try:
            # 在head中匹配含有data-testid="UserProfileSchema-test"的script标签 /html/head/script[4]
            script_element = driver.find_element_by_xpath('//head//script[@data-testid="UserProfileSchema-test"]')
            UserProfileSchema_test = script_element.get_attribute("text")
            UserProfileSchema = json.loads(UserProfileSchema_test)
        except Exception as e:
            UserProfileSchema = None
        try:
            for i in UserProfileSchema['author']['interactionStatistic']:
                if i['name'] == 'Follows':
                    followers = i['userInteractionCount']
                elif i['name'] == 'Friends':
                    following = i['userInteractionCount']
                elif i['name'] == 'Tweets':
                    tweet_num = i['userInteractionCount']
        except Exception as e:
            followers = 0
            following = 0
            tweet_num = 0

        try:
            join_date = UserProfileSchema['dateCreated']
        except Exception as e:
            join_date = ''

        try:
            additionalName = UserProfileSchema['author']['additionalName']
        except Exception as e:
            additionalName = ''

        try:
            givenName = UserProfileSchema['author']['givenName']
        except Exception as e:
            givenName = ''

        try:
            description = UserProfileSchema['author']['description']
        except Exception as e:
            description = ''

        try:
            website = UserProfileSchema['relatedLink']
        except Exception as e:
            website = ''

        try:
            image = UserProfileSchema['author']['image']['contentUrl']               
        except Exception as e:
            image = ''
        
        try:
            type = driver.find_element_by_xpath(
                '//div[contains(@data-testid,"UserProfileHeader_Items")]/span[1]').text
        except Exception as e:
            type = ''
        
        try:
            background_image_path = driver.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/a/div/div[2]/div/img')
            if background_image_path:
                background_image = background_image_path[0].get_attribute('src')
            else:
                print("No elements found")
        except Exception as e:
            background_image = ''

        print("--------------- " + user + " information : ---------------")
        print("additionalName : ", additionalName)
        print("givenName : ", givenName)
        print("image : ", image)
        print("background_image : ", background_image)
        print("Following : ", following)
        print("Followers : ", followers)
        print("Tweet num : ", tweet_num)
        print("type : ", type)
        print("Join date : ", join_date)
        print("Description : ", description)
        print("Website : ", str(website))
        data = {
            'additionalName': [additionalName],
            'givenName': [givenName],
            'image': [image],
            'background_image': [background_image],
            'following': [following],
            'followers': [followers],
            'tweet_num': [tweet_num],
            'type': [type],
            'join_date': [join_date],
            'description': [description],
            'website': [str(website)],
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', index=False, header=False)

        if i == len(users) - 1:
            driver.close()


def log_user_page(user, driver, headless=True):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_users_followers(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    followers = utils.get_users_follow(users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(followers, f)
        print(f"file saved in {file_path}")
    return followers


def get_users_following(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    following = utils.get_users_follow(users, headless, env, "following", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    with open(file_path, 'w') as f:
        json.dump(following, f)
        print(f"file saved in {file_path}")
    return following


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
