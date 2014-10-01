from tests.fixtures import *

import key

@pytest.fixture
def ms_key(gpg_keyring):
    return gpg_keyring.get_keys().values()[0]

class TestGPGKeyFromKeydata:
    def test_good_data(self, gpg_keydata):
        assert key.GPGKey.from_keydata(gpg_keydata)._keydata() == gpg_keydata

    def test_bad_data(self):
        with pytest.raises(key.KeyError):
            key.GPGKey.from_keydata("foobar")


class TestGPGKeyFromMonkeysignKeyring:
    def test_from_keyring(self, gpg_keyring, ms_key):
        gpg_key = key.GPGKey.from_monkeysign_keyring(gpg_keyring, ms_key.fpr)
        assert gpg_key.fingerprint() == ms_key.fpr

    def test_key_not_in_keyring(self, gpg_keyring):
        with pytest.raises(key.KeyError):
            key.GPGKey.from_monkeysign_keyring(gpg_keyring, "BADF00D")


# class TestGPGKeyFromMonkeysignKey:
#     def test_from_key(self, ms_key):
#         assert ms_key.fpr == GPGKey.from_monkeysign_key(ms_key).fingerprint()
