from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import gspread
import pyautogui

# 창띄우기
keyword = pyautogui.prompt("파일명 넣어주세요")

#열쇠열고 구글시트 집에 들어간다
gc = gspread.service_account(filename="keys.json")

#입력한 이름으로 시트하나 만든다
sh = gc.create(keyword)
# sh.append(["순위", "이름", "별점", "방문자리뷰","블로그리뷰" ])

#워크시트도 만들어 본다. 두개나
worksheet = sh.add_worksheet(title="A wgggggg00", rows=100, cols=20)
worksheet = sh.add_worksheet(title="A llllllll", rows=100, cols=20)

# 이 로봇이 백인탁한테 공유 승인을 한다.
sh.share('busan100@gmail.com', perm_type='user', role='writer')

browser = webdriver.Chrome("C:\chromedriver.exe")
browser.get("https://map.naver.com/v5/")
browser.implicitly_wait(10)
browser.maximize_window()

# 검색창 입력
search = browser.find_element_by_css_selector("input.input_search")
search.click
time.sleep(1)
search.send_keys(f"{keyword} 빵집")
time.sleep(1)
search.send_keys(Keys.ENTER)
time.sleep(2)

# iframe 안으로 들어가기
browser.switch_to.frame("searchIframe")

# browser.switch_to_default_content() iframe 밖으로 나오기

# iframe 안쪽을 한번 클릭하기4
browser.find_element_by_css_selector("#_pcmap_list_scroll_container").click()

# 로딩된 데이터 갯수 확인
lis = browser.find_elements_by_css_selector("li._1EKsQ")
before_len = len(lis)

while True:
    # 맨 아래로 스크롤 내린다.
    browser.find_element_by_css_selector("body").send_keys(Keys.END)

    #스크롤 사이 페이지 로딩 시간
    time.sleep(1.5)


    # 스크롤 후 로딩된 데이터 개수 확인
    lis = browser.find_elements_by_css_selector("li._1EKsQ")
    after_len = len(lis)

    print("스크롤 전", before_len, "스크롤 후", after_len)

    # 로딩된 데이터 개수가 같다면 반복 멈춤
    if before_len == after_len:
        break
    before_len = after_len

#데이터 기다리는 시간을 0으로 만들어 줘요. (데이터가 없더라도 빠르게 넘어갑니다.)
browser.implicitly_wait(0)

rank = 1
for li in lis:
    #광고 상품 아닌 것만
    if len(li.find_elements_by_css_selector("svg._2ulu3")) == 0:
        # 별점이 있는것만 크롤링
        if len(li.find_elements_by_css_selector("span._2FqTn._1mRAM > em")) > 0:
            # 가게명
            name = li.find_element_by_css_selector("span.OXiLu").text
            # 별점
            star = li.find_element_by_css_selector("span._2FqTn._1mRAM > em").text

            # 영업 시간이 있다면
            if len(li.find_elements_by_css_selector("span._2FqTn._4DbfT")) > 0:
                # 방문자수 
                try:
                    visit_review = li.find_element_by_css_selector("span._2FqTn:nth-child(3)").text
                except:
                    visit_review = "0"
                #블로그 리뷰수
                try:
                    blog_review = li.find_element_by_css_selector("span._2FqTn:nth-child(4)").text
                except:
                    blog_review = "0"
            else:
                # 방문자수 
                try:
                    visit_review = li.find_element_by_css_selector("span._2FqTn:nth-child(2)").text
                except:
                    visit_review = "0"
                #블로그 리뷰수
                try:
                    blog_review = li.find_element_by_css_selector("span._2FqTn:nth-child(3)").text
                except:
                    blog_review = "0"
            #데이터 전처리
            visit_review = visit_review.replace("방문자리뷰 ", "").replace(",","")
            blog_review = blog_review.replace("블로그리뷰 ", "").replace(",","")


            print(rank, name, star, visit_review, blog_review)
            # sh.update([rank, name, float(star), int(visit_review), int(blog_review)])
            rank = rank + 1


