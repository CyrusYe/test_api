import pytest
import requests
import json

domain_url ="https://trade.gtsuat.com"


def auth_token(username):

    url = domain_url+"/v2/user/login"

    payload = json.dumps({
      "mobilePrefix": "86",
      "password": "aa123456",
      "username": username
    })
    headers = {
      'callType': 'app',
      'lang': 'zh-CN',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text)
    response_data = response.json()
    return {
        "token" : response_data["data"]["token"],
        "username" : response_data["data"]["username"],
    }
#活動進行中測試
@pytest.mark.parametrize("username, status", [
    ("",1), #遊客
    ("15599900575",2), #未KYC
    ("15599900574",3), #未激活
    ("15599900557",4), #A9
    ("15599900564",103), #已激活未報名
    ("15599900556",104), #已報名
    ("15599900566",104)
    ])
def test_uat_battle(username,status):
    if username == "":
        token = ""
    else:
        token = auth_token(username)["token"]
    url = domain_url+"/v2/activity/tradeContest/battle/pageInfo"

    payload = json.dumps({
      "apiVerison": "v1"
    })
    headers = {
      'callType': 'app',
      'lang': 'zh-CN',
      'Content-Type': 'application/json',
      'token':token
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["data"]["stateCode"] == status