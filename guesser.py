import math
import time
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_words(file_path):
    with open(file_path,'r') as f:
        words=[line.strip().upper() for line in f.readlines()]
    return words

def get_wordle_pattern(guess,secret):
    pattern=["B"]*5
    guess_list=list(guess)
    secret_list=list(secret)
    for i in range(5):
        if guess_list[i]==secret_list[i]:
            pattern[i]="G"
            guess_list[i]=None
            secret_list[i]=None
    for i in range (5):
        if guess_list[i]==None:
            continue
        if guess_list[i] in secret_list:
            pattern[i]="Y"
            secret_index=secret_list.index(guess_list[i])
            secret_list[secret_index]=None  
    return "".join(pattern)              

def filter_words(words,guess,pattern):
    filtered_words=[]
    for w in words:
        if get_wordle_pattern(guess,w)==pattern:
            filtered_words.append(w)
    return filtered_words        

def calculate_entropy(guess,words):
    patterns=[]
    for w in words:
        patterns.append(get_wordle_pattern(guess,w))
    pattern_counter=Counter(patterns)
    total=len(words)
    entropy=0.0
    for count in pattern_counter.values():
        probability=count/total
        entropy-=probability*math.log2(probability)
    return entropy


def get_best_guess(words):
    best_word=None
    max_entropy=-1.0
    for w in words:
        entropy=calculate_entropy(w,words)
        if entropy>max_entropy:
            max_entropy=entropy
            best_word=w
    return best_word        

def scrape_row_pattern(driver,round):
    row_selector = f"div[aria-label='Row {round}']"
    row_element = driver.find_element(By.CSS_SELECTOR, row_selector)
    row_tiles = row_element.find_elements(By.CSS_SELECTOR, "div[data-testid='tile']")
    
    state_map = {"absent": "B", "correct": "G", "present": "Y"}
    pattern_list = []
    for tile in row_tiles:
        state = tile.get_attribute("data-state")
        pattern_list.append(state_map.get(state, "B"))
    return "".join(pattern_list)

driver=webdriver.Chrome()
driver.get("https://www.nytimes.com/games/wordle/index.html")
wait=WebDriverWait(driver,10)
time.sleep(5)      
try:
    accept_button = wait.until(EC.presence_of_element_located((By.ID, "fides-accept-all-button")))
    driver.execute_script("arguments[0].click();", accept_button)
except Exception:
    try:
        banner_overlay = driver.find_element(By.CSS_SELECTOR, "div[id^='fides'], div[class^='fides']")
        driver.execute_script("arguments[0].remove();", banner_overlay)
    except Exception:
        pass

time.sleep(2)

try:
    play_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='Play']")))
    play_button.click()
except Exception as e:
    print("Play button error:", e)

time.sleep(2)

try:
    close_button = driver.find_element(By.CSS_SELECTOR, "button.Modal-module_closeIcon__TcEKb")
    close_button.click()
except Exception:
    pass

time.sleep(2)
round=1
words=load_words("words.txt")

while round<=6:
    if round==1:
        guess="CRANE"
    else:
        guess=get_best_guess(words)
    body = driver.find_element(By.TAG_NAME, "body")
    body.click() 
    time.sleep(0.5)
    for letter in guess:
        body.send_keys(letter)
        time.sleep(0.1)
    body.send_keys(Keys.ENTER)
    print("Guess sent successfully!")
    time.sleep(5)
    pattern=scrape_row_pattern(driver,round)
    if pattern=="GGGGG":
        print(f"Congratulations! The word, {guess} was guessed correctly in round {round}.")
        break
    print(f"Pattern for round {round}: {pattern}")
    words=filter_words(words,guess,pattern)
    round+=1

time.sleep(10)
driver.quit()    
