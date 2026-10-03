import os
import pytest


login_test_data = [
    pytest.param(
        os.getenv("FEMCA_USERNAME"),
        os.getenv("FEMCA_PASSWORD"),
        200,
        None,
        id="valid-login"
    ),
    pytest.param(
        os.getenv("FEMCA_USERNAME"),
        "definitely_wrong_password",
        400,
        "用户名或密码错误",
        id="wrong-password"
    ),
    pytest.param(
        "definitely_wrong_user",
        "definitely_wrong_password",
        400,
        "用户名或密码错误",
        id="wrong-username"
    )
]
