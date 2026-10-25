from tests.api_client import build_headers

def test_build_headers_with_token():
    # Arrange: 準備 Token
	token = "abc123"
    # Act: 呼叫 build_headers()
	result = build_headers(token)
    # Assert: 驗證 Authorization Header
	assert result["Authorization"] == "Bearer abc123"

def test_build_headers_without_token():
    # Act: 不傳 Token
	result = build_headers()
    # Assert: 驗證回傳空 Dictionary
	assert result == {}