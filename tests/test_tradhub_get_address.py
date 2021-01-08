from . import APITestCase
from tradehub.public_client import PublicClient

DEVEL_AND_CO_SENTRY = "85.214.91.220"


class TestTradeHubGetAddress(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_address_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: dict = {
            'height': str,
            'result': {
                'type': str,
                'value': {
                    'address': str,
                    'coins': [  # Because it is a list, all entries will be checked
                        {'denom': str, 'amount': str}
                    ],
                    'public_key': {
                        'type': str,
                        'value': str
                    },
                    'account_number': str,
                    'sequence': str
                }
            }
        }

        result = self._client.get_account("swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz")
        self.assertDictStructure(expect, result)
