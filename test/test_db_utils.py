from db_utils import get_secret
import pytest
from moto import mock_aws
from botocore.exceptions import ClientError
import json


class TestSecretsManager:
    @pytest.mark.it("test secret manager returns correct secret")
    def test_secret_manager_returns_secrets(self, upload_secret):
        output = json.loads(get_secret("toteys_db_credentials", upload_secret))

        assert output == {
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "database": "test_db",
            "port": "5432",
        }

    @pytest.mark.it("test secret manager returns error when secret does not exist")
    def test_secrets_manager_for_error(self, test_secret_manager):

        with pytest.raises(ClientError) as exc:
            get_secret("toteys_db_credentials", test_secret_manager)
        err = exc.value.response["Error"]
        assert err == {
            "Message": "Secrets Manager can't find the specified secret.",
            "Code": "ResourceNotFoundException",
        }
