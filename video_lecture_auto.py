import re
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def extract_crs_aplcnt_id(url: str) -> str | None:
        match = re.search(r'crsAplcntId=([A-Z0-9]+)', url)
        if match:
            return match.group(1)
        return None

def open_keli_page(cnts_id: str, study_id: str, crsAplcntId: str):
        url = (
            "https://www.keli.kr/user/study/classroom/cnts/listLayer.do?"
            "_paramMenuNo=&crsId=O000732025084&crsMstrId=O00073&crsPtenCdv=P"
            f"&crsAplcntId={crsAplcntId}&menuNum=0"
            f"&cntsId={cnts_id}&crsStudySylbId={study_id}"
            "&resoltWidth=1300&resoltHeight=800&tab=02"
        )
        driver.execute_script(f"window.open('{url}', '_blank');")
        
        # 너무 빠른 창 생성 방지를 위한 3초 텀
        time.sleep(3)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0=ALL, 1=INFO, 2=WARNING, 3=ERROR

sys.stderr = open(os.devnull, 'w')

options = Options()
options.add_argument('--log-level=3')  # 0=ALL, 1=INFO, 2=WARNING, 3=ERROR
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(), options=options)

is_login = False

prompt = """
### 몇 차시 까지 들으셨나요? 숫자로 입력해 주세요 ###

{:<30} -> 1
{:<27} -> n    (ex. 3차시 까지 봤는데 100%가 아니면 3차시)
{:<29} -> n+1  (ex. 4차시 까지 봤는데 100%면 5차시)

=> """.format(
    "아직 1차시를 안 봤다",
    "n차시 까지 봤는데 100%가 아니면",
    "n차시 까지 봤는데 100%이면"
)

cnts_id_list = [
    "CTTCNTS0000000002532",
    "CTTCNTS0000000002533",
    "CTTCNTS0000000002534",
    "CTTCNTS0000000002535",
    "CTTCNTS0000000002536",
    "CTTCNTS0000000002537",
    "CTTCNTS0000000002538",
    "CTTCNTS0000000002539",
    "CTTCNTS0000000002540",
    "CTTCNTS0000000002541",
    "CTTCNTS0000000002542",
    "CTTCNTS0000000002543"
]

study_id_list = [
    "CRSLBT00000000044756",
    "CRSLBT00000000044757",
    "CRSLBT00000000044758",
    "CRSLBT00000000044759",
    "CRSLBT00000000044760",
    "CRSLBT00000000044761",
    "CRSLBT00000000044762",
    "CRSLBT00000000044763",
    "CRSLBT00000000044764",
    "CRSLBT00000000044765",
    "CRSLBT00000000044766",
    "CRSLBT00000000044767"
]

#input_user_id = extract_crs_aplcnt_id(input("### URL을 복사 붙여넣기 해주세요 ###\n=> "))

input_user_id = input("id: ")
input_user_pw = input("pw: ")

driver = webdriver.Chrome()
driver.get("https://www.keli.kr/cmmn/login.do")

wait = WebDriverWait(driver, 10)

# 아이디, 비번 대입 후 로그인 버튼 누르기
input_id = wait.until(EC.presence_of_element_located((By.NAME, "id")))
input_id.clear()  # 기존 내용 있으면 삭제
input_id.send_keys(input_user_id)

input_pw = wait.until(EC.presence_of_element_located((By.NAME, "password")))
input_pw.clear()
input_pw.send_keys(input_user_pw)

login_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "enter")))
login_btn.click()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user"))
    )
    is_login = True
except TimeoutException:
    is_login = False

if is_login:
    driver.get("https://www.keli.kr/user/crsAplcnt/selectListUser.do")

    wait = WebDriverWait(driver, 10)

    # 3. '수강 중' 탭 클릭
    tab = wait.until(EC.element_to_be_clickable((By.ID, "tli_02")))
    tab.click()

    # 클릭 후 페이지가 바뀔 수도 있으니 잠시 기다림
    time.sleep(2)

    # 4. 강의실 입장 버튼 요소 찾기
    # a 태그의 onclick 속성에서 crsAplcntId 값을 정규식으로 추출
    btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.c_btn.sm.blue.l_hg")))

    onclick_attr = btn.get_attribute("onclick")

    # 정규식으로 crsAplcntId 값 추출
    match = re.search(r"crsAplcntId'\s*:\s*'([^']+)'", onclick_attr)
    if match:
        crsAplcntId = match.group(1)
    else:
        print("crsAplcntId 값을 찾지 못하였습니다")

lesson = int(input(prompt))

start_idx = int(lesson) - 1

for cnts, study in zip(cnts_id_list[start_idx:], study_id_list[start_idx:]):
    open_keli_page(cnts_id=cnts, study_id=study, crsAplcntId=crsAplcntId)

input("""
### 동영상 강의를 모두 들으신 후 프로그램을 종료하여 주시기 바랍니다. ###
< 아무 키나 누르시면 프로그램이 종료 됩니다 >
""")