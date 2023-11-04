from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import random
from concurrent.futures import ThreadPoolExecutor
import re
from UserHub.helper import find_hashtags, find_usernames,str_to_int
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import asyncio
from UserHub.storages import upload_to_s3, read_json_from_s3
    







def beat_login_instagram():
    user = [("sellorbuy.shop","17derya17@"),("oceanangel.ai","17ocean7@")]

    random_user = random.choice(user)
    
    url = "https://www.instagram.com/"      
    options = Options()     
    options.add_argument('--headless=new')    
    options.add_argument("start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")    
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')   
    options.add_argument('--ignore-ssl-errors=yes')
    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/95.0.4638.69 Safari/537.36")
    driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',options=options)
    
    driver.get(url)
    sleep(5)
    try:
        user = driver.find_element(By.NAME, "username")
    
        user.send_keys(random_user[0])
    
        pwrd = driver.find_element(By.NAME,"password")
    
        pwrd.send_keys(random_user[1])
    
        driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button/div').click()
        sleep(5)
        return ("success",driver)
    except NoSuchElementException:        
        print("Element was not found!")       
        driver.quit()
        return 
    except Exception as e:
        print(f"Error: {e}")                                   
        driver.quit()
        return 
    except TimeoutException:
        driver.quit()
        return      
    
    

async def get_reels(username,driver,user):    
    await asyncio.sleep(1)
    url = f"https://www.instagram.com/{username}/reels"     
    driver.get(url)      
    sleep(5)               
    reels_urls = []
    last_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    sleep(3)
    user_infos = driver.find_element(By.CSS_SELECTOR,'div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y > div:nth-child(2) > section > main > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')
    reels_links = set()
    
    while True:
        driver.execute_script("return document.body.scrollHeight")
        sleep(2)                                        
                                                            
        user_reels = user_infos.find_elements(By.TAG_NAME,"a")
        sleep(2)     
        
        for link in user_reels:           
            
            if  link.get_attribute("href"):
                if "https://www.instagram.com/reel/" in link.get_attribute("href"):
                    
                    if link.get_attribute("href") not in reels_links:
                        temp = {}
                        reels_links.add(link.get_attribute("href"))
                        temp["url"] = link.get_attribute("href")                     
                        try:
                            watch_reel = link.find_element(By.CSS_SELECTOR, 'div._aaj_')                                                                                                                                             
                            li_elements = driver.execute_script("""
        var anchorElement = arguments[0];
        var liElements = anchorElement.querySelectorAll("li");
        var items = [];       
        
        var likeText = liElements[0].querySelector("span").textContent;
        var commentText = liElements[1].querySelector("span").textContent;
        
        items.push({"likes": likeText, "comments": commentText});
        
        return items;""", link)

                            likes = str_to_int(li_elements[0]["likes"])                  
                            temp["likes"] =  likes
                            comments = str_to_int(li_elements[0]["comments"])  
                            temp["comments"] = comments                                     
                                                             
                            try: 
                                check_watch = watch_reel.find_element(By.TAG_NAME,"span").text                             
                                
                                watch = str_to_int(check_watch)
                                temp["watch"] = watch
                                temp["engagement_rate"] = likes + comments + watch  
                            except NoSuchElementException:
                                print("Element was not found!")
                                temp["engagement_rate"] = likes + comments                
                            reels_urls.append(temp)
                        except NoSuchElementException:
                            print("Element was not found!")
                            watch_reel = link.find_element(By.CSS_SELECTOR, 'div._aajy')
                            watch = str_to_int(watch_reel.find_element(By.TAG_NAME,"span").text)
                            temp["watch"] = watch
                            temp["engagement_rate"] = watch                    
                            reels_urls.append(temp)
                                                                                   
        last_count = last_height
        sleep(2)
        
        last_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        if len(reels_urls) >= 100:
            break
        if last_count==last_height:
            break                 
    
    file_name = f"{user}-{username}-reels-data"
    upload_to_s3(reels_urls, file_name)

    return "Data was uploaded!"




async def get_instagram(username,driver,user):   
    await asyncio.sleep(1) 
    url = f"https://www.instagram.com/{username}/"           
       
    driver.get(url)
    sleep(5)          
    profile = {}
    div_element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.x7a106z'))) 
    span_info = div_element.find_element(By.CSS_SELECTOR,'span')
    
    
    profile["username"] = username
    profile["full_name"] = span_info.text                             
    
    ul_element = driver.find_element(By.CSS_SELECTOR,'ul.x78zum5')
    
    li_elements = ul_element.find_elements(By.TAG_NAME,'li')
    
    for li_element in li_elements:        
        span_element = li_element.find_element(By.TAG_NAME,'span')
        text = span_element.text
        
        li_text = li_element.text
        data = li_text.split()
        profile[data[1]] = text           
         
    user_data = {}
    infos = []        
   
    last_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    user_infos = driver.find_element(By.CSS_SELECTOR,"article.x1iyjqo2")    
        
    post_urls = []          
    while True:
        driver.execute_script("return document.body.scrollHeight")
        sleep(1)                       
        user_posts = user_infos.find_elements(By.CSS_SELECTOR,'div._ac7v._al3n')
        sleep(1)                
        for info in user_posts:                        
            href = info.find_elements(By.TAG_NAME,"a")                                                        
            sleep(1)  
            for hr in href:           
                try:                    
                    if hr.get_attribute("href") not in post_urls:
                        post = dict()
                        post_urls.append(hr.get_attribute("href"))                         
                        post["url"] = hr.get_attribute("href") 
                                                                                                
                        infos.append(post)
                except NoSuchElementException:
                    print("Element was not found")
        last_count = last_height
        sleep(2)
        last_height = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        if len(post_urls) >= 100:
            break
        if last_count==last_height:
            break   
        
    
    user_data["profile"] = profile                  
    
    user_data["posts"] = infos    
    file_name = f"{user}-{username}-posts"
    upload_to_s3(user_data,file_name)
    
    return "Data was uploaded!"

async def beat_scrape_website(username,driver,user):
    
    instagram_result, reels_result =await asyncio.gather(
        get_instagram(username, driver,user),
        get_reels(username,driver,user)
    )
    
    return instagram_result


def get_posts(url):        
    
    options = Options()            
    options.add_argument('--headless')    
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")    
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--log-level=1')        
      
    
    mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}   
    options.add_experimental_option("mobileEmulation", mobile_emulation)  
    driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',options=options)
    
    driver.get(url)
    sleep(2)
    posts = dict()                   
    
    posts["url"] = url        

    try:                                 
        user_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div:nth-child(1) > div > article._aa6a._aatb._aatd._aatf')))                
       
        
        post_time = WebDriverWait(user_post, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._akdp > div > div > a > span > time')))       
       
        posts["time"] = post_time.text
        
        post_title = WebDriverWait(user_post, 2).until(EC.presence_of_element_located((By.TAG_NAME,"h1")))             
        posts["title"] = post_title.text           
        posts["hashtags"] = find_hashtags(post_title.text)
        posts["tags"] = find_usernames(post_title.text)    
        posts["engagement_rate"] = 0
        try:
            
            post_comments = WebDriverWait(user_post, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x12nagc.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1cy8zhl.x1oa3qoh.x1nhvcw1 > a > span > span')))
            
            comments = str_to_int(post_comments.text)
            posts["comments"] = comments
            posts["engagement_rate"] += comments
        except NoSuchElementException:
            print("Element was not found!")
        
                    
        
        try:
            post_likes = WebDriverWait(user_post, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section._ae5m')))
            
            if post_likes:
                views_pattern = r'([\d,]+) views'

                likes_pattern = r'([\d,]+) likes'

                views_match = re.search(views_pattern, post_likes.text)
                if views_match:
                    views = views_match.group(1).replace(',', '')
                    posts["views"] = str_to_int(views)
                    
                        
                    posts["engagement_rate"] += str_to_int(views)                    
                        
                        
                
                likes_match = re.search(likes_pattern, post_likes.text)
                if likes_match:
                    likes = likes_match.group(1).replace(',', '')
                    posts["likes"] = str_to_int(likes)                   
                        
                    posts["engagement_rate"] += str_to_int(likes)
                    
                              
        except NoSuchElementException:
            print("Element was not found!")                  
                                           
    except NoSuchElementException:        
        print("Element was not found!")       
    except Exception as e:
        print(f"Error: {e}")                                   
    except TimeoutException:
        driver.quit()
        return      
    
    
    driver.quit()                 
    return posts
    
    
def chunk_urls(urls_list, chunk_size=10):                            
    for i in range(0, len(urls_list), chunk_size):
        yield urls_list[i:i + chunk_size]
        


def beat_process_url(username,user):    
    
    file = f"{user}-{username}-posts"
    
    user_data = read_json_from_s3(file)    
    posts = user_data["posts"]
    posts_url = [item["url"] for item in posts]    
    urls_lists = list()    
    if len(posts_url) > 100:
        urls_lists = posts_url[:100]
    else:        
        urls_lists = posts_url            
    
    url_chunks = list(chunk_urls(urls_lists, chunk_size=10))    
    all_posts = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        
        for chunk in url_chunks:
            chunk_results = list(executor.map(get_posts, chunk))
            sleep(1)
    
            for result in chunk_results:
                
                if result != None:
                    
                    all_posts.append(result)
    
    
    file_name = f"{user}-{username}-detail-posts"
    upload_to_s3(all_posts, file_name)
    
    return "Process was completed successfully"
    


















    