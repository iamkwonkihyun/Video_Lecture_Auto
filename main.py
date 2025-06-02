import re
import time
import webbrowser

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

def extract_crs_aplcnt_id(url: str) -> str | None:
    match = re.search(r'crsAplcntId=([A-Z0-9]+)', url)
    if match:
        return match.group(1)
    return None

result = extract_crs_aplcnt_id(input("### URL을 복사 붙여넣기 해주세요 ###\n=> "))

lesson = int(input("""
### 몇 차시 까지 들으셨나요? 숫자로 입력해 주세요 ###
아직 1차시를 안 봤다           -> 1
n차시 까지 봤는데 100%가 아니다 -> n    (ex. 3차시 까지 봤는데 100%가 아니면 3차시)
n차시 까지 봤는데 100%다       -> n+1  (ex. 4차시 까지 봤는데 100%면 5차시)
=> """))


def open_keli_page(cnts_id: str, study_id: str, user_id: str = result):
    url = (
        "https://www.keli.kr/user/study/classroom/cnts/listLayer.do?"
        "_paramMenuNo=&crsId=O000732025084&crsMstrId=O00073&crsPtenCdv=P"
        f"&crsAplcntId={user_id}&menuNum=0"
        f"&cntsId={cnts_id}&crsStudySylbId={study_id}"
        "&resoltWidth=1300&resoltHeight=800&tab=02"
    )
    webbrowser.open(url)
    
    # 너무 빠른 창 생성 방지를 위한 3초 텀
    time.sleep(3)

start_idx = int(lesson) - 1

for cnts, study in zip(cnts_id_list[start_idx:], study_id_list[start_idx:]):
    open_keli_page(cnts_id=cnts, study_id=study)