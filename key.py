#!/usr/bin/env python

import hashlib
import monkeysign.gpg as gpg

class Key(object):
    """A cryptographic key."""

    def __init__(self, keydata):
        """Inits the key with the given keydata.

        Args:
            keydata as string
        
        """
        # Holy crap, I had no idea this works. Epicness.
        self._keydata = lambda: keydata


    def hash(self):
        """Returns a hash of the whole key.

        Can be used to verify it hasn't been tampered with.

        Returns:
             hash as string
        
        """
        return hashlib.sha256(self._keydata()).digest()

    def fingerprint(self):
        """Returns the fingerprint of this key.

        Returns:
            fingerprint as string
        """
        raise NotImplementedError("Please use a subclass of Key.")

class KeyError(Exception): pass


class GPGKey(Key):
    """A GPG key. Use one of the static methods to create."""

    # FIXME: Is it okay for Tempkeys to use /tmp?! That folder can be read system-wide!
    # FIXME: Is the monkeysign gpg library okay to use? It seems rather dubious..

    @classmethod
    def from_keydata(cls, keydata):
        """Imports the GPG key from the given keydata, by calling gpg(1).

        Args:
            keydata: Valid ascii-armored GPG key

        Returns:
            GPGKey

        Raises:
            KeyError

        """
        key = cls(keydata)
        ring = gpg.TempKeyring()
        if not ring.import_data(keydata):
            raise KeyError("The keydata is not valid.")
        key._key = ring.get_keys().values()[0]
        return key

    @classmethod
    def from_monkeysign_keyring(cls, ms_keyring, fingerprint):
        """Imports a GPG key from a monkeysign keyring.

        Args:
            ms_keyring: Keyring from monkeysign.gpg
            fingerprint: The fingerprint identifying the key

        Returns:
            GPGKey
        
        """
        ms_key = ms_keyring.get_keys(fingerprint)
        if not ms_key:
            raise KeyError("The key with fingerprint {} is not in this keyring"
                               .format(fingerprint))
        key = cls(ms_keyring.export_data(fingerprint))
        key._key = ms_keyring.get_keys()[fingerprint]
        return key

    # @classmethod
    # def from_monkeysign_key(cls, ms_key)
    # """Imports the GPG key from a monkeysign key.

    # Args:
    #     ms_key: Key from monkeysign.gpg

    # Returns:
    #     GPGKey
    # """
    #     key = cls(None)
    #     key._key = ms_key
    #     return key

    def fingerprint(self):
        return self._key.fpr

    def __str__(self):
        return self._key.fpr
