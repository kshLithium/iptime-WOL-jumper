import requests

ROUTER_URL = "http://192.168.0.1/cgi/service.cgi"

USERNAME = "YOUR_IPTIME_ID"
PASSWORD = "YOUR_IPTIME_PASSWORD"
TARGET_MAC = "SERVER_MAC_ADDRESS"

session = requests.Session()

# 필수 헤더 보강
session.headers.update({
    "Content-Type": "application/json",
    "Origin": "http://192.168.0.1",
    "Referer": "http://192.168.0.1/ui/",
    "User-Agent": "Mozilla/5.0"
})

# 로그인 페이로드
login_payload = {
    "method": "session/login",
    "params": {
        "id": USERNAME,
        "pw": PASSWORD
    }
}

# wol 페이로드
wol_payload = {
    "method": "wol/signal",
    "params": [TARGET_MAC]
}

# 로그인 시도
res = session.post(ROUTER_URL, json=login_payload)
print("로그인 응답:", res.text)

# wol 시도
if res.status_code == 200 and '"result":"done"' in res.text:
    print("✅ 로그인 성공")

    res = session.post(ROUTER_URL, json=wol_payload)
    print("WOL 응답:", res.text)
else:
    print("❌ 로그인 실패: 공유기가 로그인 페이지로 리디렉션했거나 세션 거부됨")