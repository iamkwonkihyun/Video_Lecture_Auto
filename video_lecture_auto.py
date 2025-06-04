import re
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 페이지 오픈 함수
def open_keli_page(driver, cnts_id: str, study_id: str, crsAplcntId: str):
        url = (
            "https://www.keli.kr/user/study/classroom/cnts/listLayer.do?"
            "_paramMenuNo=&crsId=O000732025084&crsMstrId=O00073&crsPtenCdv=P"
            f"&crsAplcntId={crsAplcntId}&menuNum=0"
            f"&cntsId={cnts_id}&crsStudySylbId={study_id}"
            "&resoltWidth=1300&resoltHeight=800&tab=02"
        )
        driver.execute_script(f"window.open('{url}', '_blank');")
        
        # 너무 빠른 창 생성 방지를 위한 3초 텀
        time.sleep(1)

# 메인 함수
def main():
    
    # 유저 정보 입력
    while True:
        input_user_id = input("id: ")
        input_user_pw = getpass.getpass("pw: ")
        
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
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "user"))
            )
            break
        except:
            driver.quit()
            print("로그인 정보가 올바르지 않습니다\n다시 한번 입력해 주세요")
            continue

    driver.get("https://www.keli.kr/user/crsAplcnt/selectListUser.do")

    wait = WebDriverWait(driver, 10)

    tab = wait.until(EC.element_to_be_clickable((By.ID, "tli_02")))
    tab.click()

    btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.c_btn.sm.blue.l_hg")))

    onclick_attr = btn.get_attribute("onclick")

    # 정규식으로 crsAplcntId 값 추출
    match = re.search(r"crsAplcntId'\s*:\s*'([^']+)'", onclick_attr)
    if match:
        crsAplcntId = match.group(1)
    else:
        print("crsAplcntId 값을 찾지 못하였습니다")
        
    start_idx = int(input(prompt)) - 1
    
    print("""
[!] 강의 창 생성중입니다.
[!] 창이 여러개 생성되었다고 창을 닫지 마십시오.""")

    for cnts, study in zip(cnts_id_list[start_idx:], study_id_list[start_idx:]):
        open_keli_page(driver=driver, cnts_id=cnts, study_id=study, crsAplcntId=crsAplcntId)

    print("""
[!] 20~30분 후에 창을 새로고침 하셔서 진행도를 확인하신 후 프로그램을 종료하여 주시기 바랍니다.
[!] [enter]키를 누르시면 프로그램이 종료 됩니다""")
    
    input()
    driver.quit()

# 변수
prompt = """
[?] 몇 차시 까지 들으셨나요? 숫자로 입력해 주세요

{:<30} -> 1
{:<27} -> n    (ex. 3차시 까지 봤는데 100%가 아니면 3차시)
{:<29} -> n+1  (ex. 4차시 까지 봤는데 100%면 5차시)

("Created TensorFlow Lite XNNPACK delegate for CPU." 이라는 문장이 생겨도 무시하고 숫자를 입력하시면 됩니다)

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

if __name__ == "__main__":
    main()