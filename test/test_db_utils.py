from db_utils import get_db_secret, get_db_warehouse_secret
import pytest
from moto import mock_aws
from botocore.exceptions import ClientError
import json


class TestGetDBSecrets:
    @pytest.mark.it("test get db secrets returns correct secret")
    def test_get_db_secrets_returns_secrets(self, upload_secret):
        output = json.loads(get_db_secret(client=upload_secret))

        assert output == {
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "database": "test_db",
            "port": "0",
        }

    @pytest.mark.it("test get db secrets_ returns error when secret does not exist")
    def test_get_db_secrets_for_error(self, test_secret_manager):

        with pytest.raises(ClientError) as exc:
            get_db_secret(client=test_secret_manager)
        err = exc.value.response["Error"]
        assert err == {
            "Message": "Secrets Manager can't find the specified secret.",
            "Code": "ResourceNotFoundException",
        }


class TestGetDBWarehouseSecrets:
    @pytest.mark.it("test db warehouse returns correct secret")
    def test_get_db_warehouse_secret_returns_secrets(self, upload_secret):
        output = json.loads(get_db_warehouse_secret(client=upload_secret))

        assert output == {
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "database": "test_db",
            "port": "0",
        }

    @pytest.mark.it(
        "test get db warehouse secrets returns error when secret does not exist"
    )
    def test_secrets_manager_for_error(self, test_secret_manager):

        with pytest.raises(ClientError) as exc:
            get_db_warehouse_secret(client=test_secret_manager)
        err = exc.value.response["Error"]
        assert err == {
            "Message": "Secrets Manager can't find the specified secret.",
            "Code": "ResourceNotFoundException",
        }
