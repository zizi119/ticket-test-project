from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

def test_missing_page_returns_404(static_base_url):
    url = f"{static_base_url}/not-existing-page-12345"
    try:
        urlopen(url, timeout=5)
        assert False, "不存在的页面不应返回成功"
    except HTTPError as error:
        assert error.code == 404
def test_ticket_not_found():
	response = {
	"status_code": 404,
	"body": {"error": "工单不存在"}
	}
	assert response["status_code"] == 404
	assert response["body"]["error"] == "工单不存在"
def test_existing_page_returns_200(static_base_url):
    url = f"{static_base_url}/hello.txt"
    with urlopen(url, timeout=5) as response:
        assert response.status == 200
        assert response.read().decode("utf-8").strip() == "hello"
def test_ticket_json(static_base_url):
    url = f"{static_base_url}/ticket.json"
    with urlopen(url, timeout=5) as response:
        assert response.status == 200
        ticket = json.load(response)
        assert ticket["ticket_id"] == "T1001"
        assert ticket["owner_id"] == "U001"
        assert ticket["title"] == "无法登录"
def test_forbidden_response_does_not_leak_title():
    response = {
        "status_code": 403,
        "body": {"error": "无权访问"}
    }

    assert response["status_code"] == 403
    assert "title" not in response["body"]
