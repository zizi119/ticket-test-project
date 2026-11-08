from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
import pytest
import os
def make_ticket_request(base_url, ticket_id, user_id=None):
    headers = {}
    if user_id is not None:
        headers["X-User-Id"] = user_id

    return Request(
        f"{base_url}/tickets/{ticket_id}",
        headers=headers,
    )
def test_owner_can_read_ticket(base_url):
    request = make_ticket_request(base_url,"T1001", "U001")
    with urlopen(request, timeout=5) as response:
        assert response.status == 200
        ticket = json.load(response)
        assert ticket["ticket_id"] == "T1001"
        assert ticket["owner_id"] == "U001"
def test_other_user_cannot_read_ticket(base_url):
    request = make_ticket_request(base_url,"T1001", "U002")
    try:
        urlopen(request, timeout=5)
        assert False, "其他用户不应读取这张工单"
    except HTTPError as error:
        assert error.code == 403
        body = json.load(error)
        assert body["error"] == "无权访问"
        assert "title" not in body
        assert "owner_id" not in body
def test_ticket_does_not_exist(base_url):
    request = make_ticket_request(base_url,"T9999", "U001")
    try:
        urlopen(request, timeout=5)
        assert False, "不存在的工单不应返回成功"
    except HTTPError as error:
        assert error.code == 404
        body = json.load(error)
        assert body["error"] == "工单不存在"
def test_admin_can_read_ticket(base_url):
    request = make_ticket_request(base_url,"T1001", "admin")
    with urlopen(request, timeout=5) as response:
        assert response.status == 200
        body = json.load(response)
        assert body["ticket_id"] == "T1001"
        assert body["title"] == "无法登录"
def test_missing_user_cannot_read_ticket(base_url):
    request = make_ticket_request(base_url,"T1001")
    try:
        urlopen(request, timeout=5)
        assert False, "未带用户标识的请求不应读取工单"
    except HTTPError as error:
        assert error.code == 403
        body = json.load(error)
        assert body["error"] == "无权访问"
        assert "title" not in body
def test_valid_format_ticket_does_not_exist(base_url):
    request = make_ticket_request(base_url,"T7878", "U001")

    try:
        urlopen(request, timeout=5)
        assert False, "不存在的工单不应返回成功"
    except HTTPError as error:
        assert error.code == 404
        body = json.load(error)
        assert body["error"] == "工单不存在"
@pytest.mark.parametrize(
    "ticket_id",
    ["1234", "T12", "T111111111"],
)
def test_invalid_ticket_id_format(base_url,ticket_id):
    request = make_ticket_request(base_url,ticket_id, "U001")

    try:
        urlopen(request, timeout=5)
        assert False, "格式错误的工单编号不应请求成功"
    except HTTPError as error:
        assert error.code == 400
        body = json.load(error)
        assert body["error"] == "工单编号格式错误"