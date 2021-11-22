"""
Uses Selenium - headless
Very efficient and works perfectly
current score, with Target [UPDATE] and many more

Drawback : URL has to be modified everytime for each match [UPDATE] Not anymore
Can be run during or after the match

"""

from tkinter import *
from tkinter import messagebox
import threading

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime

def press():
    time.sleep(2)
    start_time = time.time()
    elapsed_time = 0
    while True: # elapsed_time<=6:
        pyautogui.click(x=1002, y=500)
        time.sleep(1)
        pyautogui.click(x=1000, y=502)
        time.sleep(1)
        pyautogui.click(x=1002, y=498)
        pyautogui.move(0, -6, duration=0.2)
        pyautogui.move(-6, 0, duration=0.2)
        pyautogui.move(0, 6, duration=0.2)
        pyautogui.move(6, 0, duration=0.2)
        elapsed_time = time.time() - start_time
        # print('Elapsed t'd9if'
        #  ime :', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        pyautogui.doubleClick(x=1000, y=500)
        print('Elapsed time 😊:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), " at ", datetime.now().time())
        time.sleep(240)


def countdown(t):
    global check_for_win
    seconds = 10000
    while seconds:
        current_date = datetime.today().day
        current_month = datetime.today().month
        if current_month == 4:
            current_month = 'Apr'
        elif current_month == 5:
            current_month = 'May'
        current_year = datetime.today().year

        if t == '07:30':
            matcht = '19:30'
        elif t == '03:30':
            matcht = '15:30'
        else:
            matcht = '18:00'

        match_time = datetime.strptime(f'{current_month} {current_date} {current_year}  {matcht}', '%b %d %Y %H:%M')

        nowdate = datetime.now()
        # print(nowdate)
        count = int((match_time - nowdate).total_seconds())

        days = count // 86400
        hours = (count - days * 86400) // 3600
        minutes = (count - days * 86400 - hours * 3600) // 60
        seconds = count - days * 86400 - hours * 3600 - minutes * 60
        if days < 0:
            countdown_lbl.pack(fill=X, expand=1)
            countdown_lbl.config(text="Match started")
            seconds = 0
            continue
        if hours < 10:
            hours = '0' + str(hours)
        if days < 10:
            days = '0' + str(days)
        if minutes < 10:
            minutes = '0' + str(minutes)
        if seconds < 10:
            seconds = '0' + str(seconds)
        countdown_lbl.pack(fill=X, expand=1)
        if days != '00':
            countdown_lbl.config(text=f"{days}days {hours}:{minutes}.{seconds} to go...")
            # print("{} days {} hours {} minutes {} seconds left".format(days, hours, minutes, seconds))
        else:
            countdown_lbl.config(text=f"{hours}:{minutes}.{seconds} to go...")
            # print("{}:{}.{} to go...".format(hours, minutes, seconds))
        time.sleep(1)
    next_match_lbl.destroy()
    team_score.destroy()
    player_lbl.destroy()
    score.config(text='"00:00.00 to go..."\n\nMatch Started\n\nLoading the live match details\n\nPlease Wait for 2mins..')
    countdown_lbl.destroy()
    time.sleep(120)
    getltp(0)


def almost_start_of_match(url):
    driver.get(url)
    wait200 = WebDriverWait(driver, 5)
    next_match_lbl.pack(fill=X, expand=1)
    next_match_lbl.config(text="\nGetting upcoming match details\n\n\n\n\nPlease wait...")
    try:
        wait200.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="matchCenter"]/div[3]/div[2]/div[3]/div[1]/div[3]')))
        Next_Match = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[2]/h1').text
        Next_Match_venue = driver.find_element_by_xpath(
            '//*[@id="matchCenter"]/div[2]/div/a[2]/span/span[1]').text
        Next_Match_venue_city = driver.find_element_by_xpath(
            '//*[@id="matchCenter"]/div[2]/div/a[2]/span/span[2]/span').text
        Next_Match_when = driver.find_element_by_xpath(
            '//*[@id="matchCenter"]/div[2]/div/span[4]/span[1]').text
        Next_Match_time = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[2]/div/span[4]/span[2]').text
        driver.execute_script("window.stop();")
    except Exception as e:
        print("Exception :", e)
        Next_Match = ''
        Next_Match_time = ''
        Next_Match_venue = ''
        Next_Match_venue_city = ''
        Next_Match_when = ''
    try:
        Toss = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[3]/div[2]/div[3]/div[2]').text
    except:
        Toss = ''
    if Next_Match_when != '':
        print(Next_Match)
        if ' - Live Cricket Score, Commentary' in Next_Match:
            Next_Match = Next_Match.replace(' - Live Cricket Score, Commentary', '')
        # print(Next_Match)
        next_match_lbl.config(
            text=f"\nUpcoming Match: \n{Next_Match}\nat: {Next_Match_venue}{Next_Match_venue_city}\n{Next_Match_when} {Next_Match_time}")
        if Toss !='':
            score.config(text=f'{Toss}', font=('calibri', 50, 'bold'))
        if '07:30 PM' in Next_Match_time:
            countdown('07:30')
        elif '03:30 PM' in Next_Match_time:
            countdown('03:30')


def next_match():
    live_lbl.destroy()
    wait100 = WebDriverWait(driver, 5)
    # wait200 = WebDriverWait(driver, 5)
    driver.get('https://www.cricbuzz.com/')
    wait100.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/nav/a[3]')))
    driver.execute_script("window.stop();")
    driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div/nav/a[3]').click()
    url = driver.current_url
    almost_start_of_match(url)


def getltp(stop):
    global driver
    options = Options()
    options.headless = True

    # Don't allow images to load
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"

    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('start-maximized')
    # PATH = f"{os.path.normpath(os.getcwd() + os.sep + os.pardir)}/chromedriver.exe"
    PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=PATH, desired_capabilities=capa)
    wait1 = WebDriverWait(driver, 2000)
    driver.get('https://www.cricbuzz.com/')
    wait1.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/nav/a[2]')))
    driver.execute_script("window.stop();")
    score.config(text="Connected...🎶", font=('calibri', 90, 'bold'))

    # To keep the screen active
    # t2 = threading.Thread(target=press)
    # t2.daemon = True
    # t2.start()

    # if count():
    print(driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div/nav/a[2]').text)
    if 'Toss' in (driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div/nav/a[2]').text):
        driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div/nav/a[2]').click()
        url = driver.current_url
        almost_start_of_match(url)
    elif 'Preview' in (driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div/nav/a[2]').text):
        driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div/nav/a[2]').click()
        url = driver.current_url
        almost_start_of_match(url)
    driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div/nav/a[2]').click()
    url = driver.current_url

    check_for_win =  0
    start_time = time.time()
    score.config(text=f"Reading the details for you ✔", font=('calibri', 70, 'bold'))

    while True:
        live_lbl.config(text="LIVE", font=('calibri', 15, 'bold'), fg="red")
        wait_won = WebDriverWait(driver, 6)
        wait = WebDriverWait(driver, 12)
        if check_for_win == 1:
            continue
        # driver.get('https://www.cricbuzz.com/live-cricket-scores/35678/csk-vs-rcb-19th-match-indian-premier-league-2021')
        driver.get(url)

        # If match is not live/ finished
        if check_for_win == 0:
            try:
                # score.config(text="Next match yet to start!\n[Please wait] While we get last match details...", font=('calibri', 40, 'bold'))
                wait_won.until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="matchCenter"]/div[3]/div[2]/div[2]/div[2]')))
                Match_result = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[3]/div[2]/div[2]/div[2]').text
                Team1_score = driver.find_element_by_xpath(
                    '//*[@id="matchCenter"]/div[3]/div[2]/div[2]/div[1]/div[1]/h2[1]').text
                Team2_score = driver.find_element_by_xpath(
                    '//*[@id="matchCenter"]/div[3]/div[2]/div[2]/div[1]/div[1]/h2[2]').text
                driver.execute_script("window.stop();")
                print("Match is over!")
            except:
                # score.config(text="[Wait] Match seems to be alive!", font=('calibri', 40, 'bold'))
                # print("Match is live")
                Match_result = ''
                Team1_score = ''
                Team2_score = ''
            try:
                Player_of_the_Match = driver.find_element_by_xpath(
                    '//*[@id="matchCenter"]/div[3]/div[2]/div[2]/div[3]/a').text
            except:
                Player_of_the_Match = ''
            if Match_result != '':
                check_for_win = 1
                score.config(text=f"{Match_result}", font=('calibri', 50, 'bold'), fg="red")
                team_score.pack(fill=X, expand=1)
                player_lbl.pack(fill=X, expand=1)
                team_score.config(text=f'{Team1_score}\n{Team2_score}')
                player_lbl.config(text=f'\nPlayer of the Match:\n{Player_of_the_Match}')
                next_match()
                continue

        # wait.until(EC.presence_of_element_located(
        #     (By.XPATH, '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/h2')))
        # wait.until(EC.visibility_of_element_located(
        #     (By.XPATH, '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/h2')))
        # wait.until(EC.visibility_of_element_located(
        #     (By.XPATH, '//*[@id="matchCenter"]/div[2]/div/a[2]/span/span[1]')))
        try:
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[4]/div/div/span[2]')))  # Recent thing
        except:
            continue
        try:
            Score = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/h2').text
            Target = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]/h2').text
            Recent = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[4]/div/div/span[2]').text
        except Exception as e:
            Score = ''
            Target = ''
            Recent = ''
        try:
            Curr_RR = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/span[1]/span[2]').text
        except Exception as e:
            Curr_RR = ''
        try:
            Req_RR = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/span[2]/span[2]').text
        except Exception as e:
            Req_RR = ''
        try:
            Batsman = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/a').text
            Batsman_score = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]').text
            Batsman_score_in_balls = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]').text
        except Exception as e:
            Batsman = ''
            Batsman_score = ''
            Batsman_score_in_balls = ''
        try:
            Batsman_second = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/a').text
            Batsman_second_score = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]').text
            Batsman_second_score_in_balls = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[1]/div[3]/div[3]').text
        except Exception as e:
            Batsman_second = ''
            Batsman_second_score = ''
            Batsman_second_score_in_balls = ''
        try:
            Bowler = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/a').text
            Bowler_overs = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]').text
            Bowler_wickets = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div[5]').text
            Bowler_runs = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div[4]').text
            Commentry = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[2]/h1').text
            Venue = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[2]/div/a[2]/span/span[1]').text
            City = driver.find_element_by_xpath('//*[@id="matchCenter"]/div[2]/div/a[2]/span/span[2]/span').text
            Last_wicket = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[3]/div/div[3]/span[2]').text
            reqd_runs = driver.find_element_by_xpath(
                '//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]').text
            '//*[@id="matchCenter"]/div[3]/div[2]/div[2]/div[2]'
        except Exception as e:
            Bowler = ''
            Bowler_overs = ''
            Bowler_wickets = ''
            Bowler_runs = ''
            Commentry = ''
            Venue = ''
            City = ''
            reqd_runs = ''
            Last_wicket = ''
        if Score != '':
            # check_for_win = 1
            score.config(text=f"{Score}", font=('calibri', 100, 'bold'))
            live_lbl.pack(fill=X, expand=1)
        if Curr_RR != '':
            rr.pack(fill=X, expand=1)
            rr.config(text=f"Current RR : {Curr_RR}")
            if Req_RR != '':
                rr.config(text=f"Cur. RR : {Curr_RR} : Reqd. RR : {Req_RR}")
        if Target != '':
            target.pack(fill=X, expand=1)
            target.config(text=f"Target : {Target}\n{reqd_runs}")
        if Recent != '':
            recent.pack(fill=X, expand=1)
            recent.config(text=f"Recent : {Recent}")
        if Last_wicket != '':
            last_wicket.pack(fill=X, expand=1)
            last_wicket.config(text=f"Last Wicket : {Last_wicket}")
        if Batsman != '':
            batsman.pack(fill=X, expand=1)
            if Batsman_second == '':
                batsman.config(
                    text=f"Batsman : \n{Batsman}* - {Batsman_score} Runs in {Batsman_score_in_balls} balls\nOUT! {Last_wicket}")
            else:
                batsman.config(
                    text=f"Batsman : \n{Batsman}* - {Batsman_score} Runs in {Batsman_score_in_balls} balls\n{Batsman_second} - {Batsman_second_score} Runs in {Batsman_second_score_in_balls} balls")
        if Bowler != '':
            bowler.pack(fill=X, expand=1)
            bowler.config(text=f"Bowler : \n{Bowler} - ({Bowler_wickets} - {Bowler_runs}), in {Bowler_overs} over(s)")
        if Commentry != '':
            commentry.pack(fill=X, expand=1)
            if ' - Live Cricket Score, Commentary' in Commentry:
                Commentry = Commentry.replace(' - Live Cricket Score, Commentary', '')
            commentry.config(text=f"{Commentry}\nVenue : {Venue}{City}")
        driver.execute_script("window.stop();")
        time_took_for_refresh = time.time() - start_time
        if Target != '':
            print(f"[Score Refreshed in {time.strftime('%S', time.gmtime(time_took_for_refresh))}s] - {Target},  {Score}, updated at {datetime.now().time()}")
        else:
            print(f"[Score Refreshed in {time.strftime('%S', time.gmtime(time_took_for_refresh))}s] - 1st innings : {Score}, updated at {datetime.now().time()}")
        for i in range(4):
            live_lbl.config(text="LIVE", font=('calibri', 15, 'bold'), fg="black")
            time.sleep(0.25)
            live_lbl.config(text="LIVE", font=('calibri', 15, 'bold'), fg="yellow")
            time.sleep(0.25)
        # time.sleep(1)
        start_time = time.time()


def start(check):
    score.config(text="Connecting...🎶")
    t1 = threading.Thread(target=lambda: getltp(0))
    if check == 1:
        s1.destroy()
        # s2.pack(fill=X, expand=1)
        t1.daemon = True
        t1.start()
    if check == 0:
        exit()
        s2.destroy()
        s3 = Button(main_root, text='Start showing IPL score', command=lambda: start(1))
        s3.pack(fill=X, expand=1)


main_root = Tk()
main_root.title("IPL live score")
main_root.state('zoomed')

score = Label(main_root, text='Click start below 🤔', font=('calibri', 100, 'bold'), fg="blue", bg="#202020")
rr = Label(main_root, text='', font=('calibri', 15, 'bold'), fg="red", bg="#202020")
target = Label(main_root, text='', font=('calibri', 20, 'bold'), fg="yellow", bg="#202020")
recent = Label(main_root, text='', font=('calibri', 30, 'bold'), fg="gold", bg="#202020")
last_wicket = Label(main_root, text='', font=('calibri', 14, 'bold'), fg="red", bg="#202020")
batsman = Label(main_root, text='', font=('calibri', 30, 'bold'), fg="#3bdbff", bg="#202020")
bowler = Label(main_root, text='', font=('calibri', 30, 'bold'), fg="orange", bg="#202020")
commentry = Label(main_root, text='', font=('calibri', 16, 'bold'), fg="lightgreen", bg="#202020")
s1 = Button(main_root, text='Start showing IPL score', command=lambda: start(1))
s2 = Button(main_root, text='Stop showing IPL score', command=lambda: start(0))

team_score = Label(main_root, text='', font=('calibri', 30, 'bold'), fg="#3bdbff", bg="#202020")
player_lbl = Label(main_root, text='', font=('calibri', 30, 'bold'), fg="yellow", bg="#202020")
next_match_lbl = Label(main_root, text='', font=('calibri', 30, 'bold'), fg="orange", bg="#202020")
countdown_lbl = Label(main_root, text='', font=('calibri', 50, 'bold'), fg="grey", bg="#202020")
live_lbl = Label(main_root, text='', font=('calibri', 30, 'bold'), fg="red", bg="#202020")

score.pack(fill=X, expand=1)
s1.pack(fill=X, expand=1)

start(1)

main_root.config(bg="#202020")

main_root.mainloop()
