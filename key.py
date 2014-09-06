#!/usr/bin/env python

import hashlib
import monkeysign.gpg as gpg

class KeyError(Exception):
    pass

class Key(object):
    """A cryptographic key."""

    def __init__(self, keydata):
        """Inits the key with the given keydata.

        Args:
            keydata as string
        
        """
        # Holy crap, I had no idea this works. Epicness.
        self._keydata = lambda: keydata


    def keyhash(self):
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

    def __str__(self):
        return self._key.fpr


class GPGKey(Key):
    """A GPG key."""

    def __init__(self, keydata):
        """Imports the GPG key from the given keydata, by calling gpg(1).

        Args:
            keydata: Valid ascii-armored GPG key

        Raises: GPGError

        """
        super(GPGKey, self).__init__(keydata)
        ring = gpg.TempKeyring()
        if not ring.import_data(keydata):
            raise GPGError("The keydata is not valid.")

        self._key = ring.get_keys().values()[0]

    def fingerprint(self):
        return self._key.fpr


class GPGError(Exception): pass
