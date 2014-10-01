import key as key_m

import pytest
import monkeysign.gpg as gpg

@pytest.fixture
def gpg_keydata():
    """Test gpg public key."""
    with open('tests/example_pubkey.asc') as f:
        return f.read()

@pytest.fixture
def gpg_keyring(gpg_keydata):
    """A keyring with one example private key."""
    ring = gpg.TempKeyring()
    if not ring.import_data(gpg_keydata):
        raise KeyImportError()
    return ring

@pytest.fixture
def key(gpg_keydata):
    return key_m.GPGKey.from_keydata(gpg_keydata)


class KeyImportError(Exception): pass
