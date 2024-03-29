from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from codes import *
from selenium.webdriver.support.ui import Select
import random
from trades import *
from main_config import *
from multiprocessing import Pool
from selenium.webdriver.common.keys import Keys as KEYS
import sys

import os
print('Number of CPUs in the system: {}'.format(os.cpu_count()))
file1 = open("testresults.txt", "w")


def login(i, driver):
        # userid = WebDriverWait(driver, 2).until(
        # EC.presence_of_element_located((By.XPATH, '// *[ @ id = "TextField9"]')))
        # userid = driver.find_element_by_xpath('// *[ @ id = "TextField9"]')
        userid = driver.find_element(by= By.XPATH, value='/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div/input')
        # print("Found UserId Col")
        password = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/input')))
        # print("Found Password Col")
        loginbutton = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/button/span')))
        # print("Found Login Button")
        userid.clear()
        userid.click()
        userid.send_keys(username)
        # print("Entered a UserId")
        password.clear()
        password.click()
        password.send_keys(str(i))
        print("Logged in successfully at tab ", i)
        loginbutton.click()
        # driver.execute_script("document.body.style.zoom='90%'")

def check_data(i, driver):
    # loading_tagding_tag = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[1]/span[2]')
    if i >= 3:
        return
    driver.switch_to.window("tab" + str(i) + "")
    try:
        loadingtag = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-200"))
        )
        print("Data Being Fetched Successfuly")
    except:
        print("Data Not Being Fetched at tab : ", i)


def select_leg(i, driver):
    # driver.switch_to.window("tab" + str(i) + "")
    # time.sleep(1)randomise_dropdown(driver, 'Dropdown97')
    try:
        symbol1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div')))
        symbol1.click()
        symbol1list = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div/div')))
        legoptions = symbol1list.find_elements(by=By.XPATH, value="*")
    except:
        select_leg(i, driver)
        return
    # print(legoptions)
    # selected_leg = random.randint(0, len(legoptions)-1)
    selected_leg = random.randint(1, 1)
    # selected_leg = 1
    # print(selected_leg)
    time.sleep(0.4)
    # print("leg", selected_leg)
    try:
        legoptions[selected_leg].click()
    except:
        select_leg(i, driver)
        return
    # symbol1.select_by_index(random(legoptions.size()))
    # print(legoptions)
    s = "Selected Leg : " + str(selected_leg + 1) + "\n"
    file1.write(s)
    select_strategy(i, driver,selected_leg)

def find_name(strat_item):
    first = strat_item.find_elements(by=By.XPATH, value="*")
    second = first.find_elements(by=By.XPATH, value="*")
    return second.get_attribute('innerHTML')


def select_strategy(i,driver,leg):
    WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/span[1]'))).click()
    strategylist = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div/div')))
    # print(strategylist)
    try:
        stratoptions = strategylist.find_elements(by=By.XPATH, value="*")
    except:
        select_strategy(i, driver, leg)
        return
    # print(stratoptions)
    # print(legoptions)
    selected_strat = random.randint(0, len(stratoptions)-1)
    # selected_strat = 3
    opn = selected_strat+1
    selected_strat_name = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div/button["+str(opn)+"]/span/span"))).get_attribute('innerHTML')
    # selected_strat = 8
    print("Running Strategy : ", selected_strat_name)
    s = "Running Strategy : " + str(selected_strat_name)
    file1.write(s)
    time.sleep(0.2)
    try:
        stratoptions[selected_strat].click()
    except:
        select_strategy(i, driver, leg)
        return
    # print(selected_leg)
    css241_selections(i, driver,leg, selected_strat, selected_strat_name)

def randomise_dropdown(driver, name):
    try:
        symbol1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, name))).click()
        time.sleep(0.2)
        strategylist = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div/div')))
        # print(strategylist)
        stratoptions = strategylist.find_elements(by=By.XPATH, value="*")
        if(len(stratoptions)==0):
            s = " No options Available \n"
            file1.write(s)
            return "NOOP"
    except:
        randomise_dropdown(driver, name)
        return
    # print(len(stratoptions))
    selected_strat = random.randint(0, len(stratoptions)-1)
    # if selected_strat - 4 >= 0:
    #     selected_strat = selected_strat - 4
    time.sleep(0.2)
    opn = selected_strat+1
    selected_opt_name = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div/button["+str(opn)+"]/span/span"))).get_attribute('innerHTML')
    # selected_strat = 8
    # time.sleep(0.2)
    try:
        actions = ActionChains(driver)
        if selected_strat + 4 < len(stratoptions):
            actions.move_to_element(stratoptions[selected_strat+4]).perform()
            time.sleep(0.1)
        else:
            actions.move_to_element(stratoptions[selected_strat]).perform()
            time.sleep(0.1)
        stratoptions[selected_strat].click()
    except:
        # time.sleep(0.4)
        randomise_dropdown(driver, name)
        return
    # if 'Select' in symbol1.get_attribute('innerHTML'):
    #     randomise_dropdown(driver, name)
    print(" ->  : ", selected_opt_name)
    s = " ->  : " + str(selected_opt_name)
    file1.write(s)


def randomise_new_dropdown(driver, path):
    sym = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, path)))
    sym.click()
    chosen_sym = random.choice(freq_sym)
    time.sleep(1)
    sym.send_keys(chosen_sym)
    time.sleep(1)
    sym.send_keys(KEYS.ARROW_UP)
    time.sleep(1)
    sym.send_keys(KEYS.ENTER)
    time.sleep(1)
    # sym = WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH, name_for_new_dropdown[0])))
    # get_name = sym.get_attribute("innerHTML")
    # print(" ->  : ", get_name)
    # s = " ->  : " + str(get_name)
    # file1.write(s)
    return chosen_sym

def css241_selections(i, driver,leg, strat, strat_name):
    if leg == 0:
        # randomise_dropdown(driver, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/div/span[1]'
        op = randomise_new_dropdown(driver, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[1]/div[2]/input')
        if op == "NOOP":
            return
        # '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[2]/div/span[2]'
        # op = randomise_dropdown(driver, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div/div[1]')
        # if op == "NOOP":
        #     return
        op = randomise_dropdown(driver, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[2]/div/span[1]')
        if op == "NOOP":
            return
        op = randomise_dropdown(driver, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[3]/div/span[1]')
        if op == "NOOP":
            return
        op = randomise_dropdown(driver, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[4]/div/span[1]')
        if op == "NOOP":
            return
        op = randomise_dropdown(driver, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div/div/span[2]')
        if op == "NOOP":
            return
    elif leg == 1:
        if strat_name == "EQ2FB":
            op = randomise_new_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/input')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div[2]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div/div/span[1]')
            if op == "NOOP":
                return
        elif strat_name == "F2EQB":
            op = randomise_new_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/input')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div[1]/div[2]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div/div/span[2]')
            if op == "NOOP":
                return
        elif strat_name == "F2FB1" or strat_name == "F2FI" or strat_name == "F2FSP":
            op = randomise_new_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div/div/span[2]')
            if op == "NOOP":
                return
        elif strat_name == "STD" or strat_name == "STG":
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_new_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[1]/div/div/div[1]/div[2]/input')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[2]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[3]/div/span[1]')
            if op == "NOOP":
                return
            if strat_name == "STG":
                op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[2]/div[3]/div/span[1]')
                if op == "NOOP":
                    return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[4]/div[1]/div/div/span[1]')
            if op == "NOOP":
                return
        elif strat_name == "ORS":
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_new_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[1]/div/div/div[1]/div[2]/input')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[2]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[3]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[4]/div/span[1]')
            if op == "NOOP":
                return
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div[5]/div/div/input'))).send_keys(1)
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[2]/div[4]/div/span[1]')
            if op == "NOOP":
                return
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[2]/div[5]/div/div/input'))).send_keys(1)
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[4]/div[1]/div/div/span[2]')
            if op == "NOOP":
                return
        elif strat_name == "ODS":
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div[2]/div/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_new_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[1]/div/div/div[1]/div[2]/input')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[3]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]/div[4]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div[3]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div[4]/div/span[1]')
            if op == "NOOP":
                return
            op = randomise_dropdown(driver,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/div/div/span[1]')
            if op == "NOOP":
                return
    else:
        return

    #add strategy
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/button/span'))).click()
    result = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/div/div/div/div[2]/span/span'))).get_attribute('innerHTML')
    s = "\n" + result + "\n"
    file1.write(s)
    print(result)
    # time.sleep(1)


def openchrome_and_openchat(input):
        #global input_box
        times = 8
        driver = webdriver.Chrome()
        for i in range(1):
            driver.execute_script("window.open('about:blank','tab"+str(i)+"');")
            driver.switch_to.window("tab"+str(i)+"")
            driver.get(test_path)
            # driver.execute_script("document.body.style.zoom='90%'")
            # driver.switch_to.window("tab" + str(i) + "")
            # time.sleep(1)
            login(i, driver)
            print("Opened Testing Environment ")

        # for i in range(times):
        #     check_data(i, driver)
        for i in range(times):
            select_leg(i, driver)
            time.sleep(8)

        # for i in range(times):
        #     automate_trades(i, driver, times)
        automate_trades(i, driver, times)
        # file1.close()
        # driver.quit()
        # sys.exit()



# def run_complex_operations(operation, input, pool):


# processes_pool = Pool(5)
# processes_pool.map(openchrome_and_openchat, range(1))
# processes_pool.close()
# processes_pool.terminate()

openchrome_and_openchat(range(5))

# run_complex_operations(openchrome_and_openchat(), range(5),  processes_pool)
# js = "document.evaluate('/html/body/div[2]/p',document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null,).singleNodeValue;"
# js = """
#   var elm = arguments[0], txt = arguments[1];
#   elm.style.display = "none";
#   """
# driver.execute_script(js, css241_feilds, "Hello")
# root > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(3) > div:nth-child(1) > div > div:nth-child(1)

# if leg == 0:
#     css241_feilds = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located(
#             (By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div')))
# elif leg == 1:
#     if strat < 2:
#         css241_feilds = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div[1]')))
#     if strat >= 2 and strat < 5:
#         css241_feilds = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]')))
#     if strat >= 5 and strat < 8:
#         css241_feilds = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]')))
#     else:
#         css241_feilds = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div[1]')))
#
# else:
#     css241_feilds = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located(
#             (By.XPATH, '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[3]/div[1]')))
# css241_feilds_list = css241_feilds.find_elements(by=By.XPATH, value="*");
#
# print(len(css241_feilds_list))
# for i in range(len(css241_feilds_list)):
#     field_lb_dr = css241_feilds_list[i].find_elements(by=By.XPATH, value="*");
#     print(field_lb_dr)


#Expiry change with persistent change
#Strike 1 Strike 2, irrelevent options
#zoomout for options
#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