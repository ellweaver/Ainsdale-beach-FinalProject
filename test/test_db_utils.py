from db_utils import get_secret
import pytest
from moto import mock_aws
import json


class TestSecretsManager:
    @pytest.mark.it("test secret manager returns correct secret")
    def test_secret_manager_returns_secrets(self, upload_secret):
        output = json.loads(get_secret(upload_secret))

        assert output == {
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "database": "test_db",
            "port": "5432",
        }
