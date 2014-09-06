from tests.fixtures import *

import key

class TestGPGKey:
    def test_good_data(self, gpg_keydata):
        assert key.GPGKey(gpg_keydata)._keydata() == gpg_keydata

    def test_bad_data(self):
        with pytest.raises(key.GPGError):
            key.GPGKey("foobar")
