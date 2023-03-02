import requests
import json

urls = {
    "enflasyon":"https://api.matriksdata.com/dumrul/v1/inflation-rates?mid=1677495874423&ngsw-bypass=true",
    "url1":"https://api.matriksdata.com/dumrul/v1/topach.gz?mid=1677494050763&ngsw-bypass=true",
    "page":"https://api.matriksdata.com/dumrul/v2/news/search/page.gz?mid=1677496590577&ngsw-bypass=true&content=true&page=0&pageSize=50&qid=48b3a7ad-a0df-4514-979b-013b6740c209"
}

headers = {"Authorization": "jwt eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYzODEzMTAxNjM2Nzk1NDA4NSIsImlzcyI6Ik1BVFJJS1MiLCJzdWIiOiIwNTA1MDc3MDc2NiIsImNsaSI6IkgiLCJpYXQiOjE2Nzc0OTQwMzYsIm5iZiI6MTY3NzQ5MzQzNiwiZXhwIjoxNjc3NTEyNjM2fQ.nC7ejxKourKlfChAZwYxsqUXCf54_W5291i4Jgjx9mM-0fQ32I79GGg6lZSq-7uI0_TMf-N_Sco9tlPaxIexJGAhJ6ErYLOHDfRJl-pFI_sMIjWtmoLmZiZkEDdkQEMdTCsCTAtk3x0nkaIPHGH-9yTZ9nECXKVRu70yEhTuGZkR-vzMkdOzseHcKoRqReOq7Ek6ERk6sbDtZAvuSn5vwPT9a1Vzle5PgiF5iWHJEHWUj-JNAu27SkgGVI09wyy5bZvyZcBgWgIbcsBqXf8gDedDtreopCIbRhz7q_NiwyTeyqLW2-5EKqE7LPW-7GR4At0UUwNDxIHK4tbIKfFJgw"}
source = open("source.html","w")
res = requests.post(urls["enflasyon"], headers=headers)
dt = json.loads(res.text)
for sym in dt:
    print(sym["symbol"]["TEFE"]["monthlyChange"])
    # print(sym["symbol"]["TUFE"])

source.write(res.text)
source.close()
print(res.status_code)