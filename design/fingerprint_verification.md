# Process description of fingerprint verification

1. Key is transferred from server to client
2. Server displays fingerprint randomart
3. Client generates three fake fingerprints
4. Client shows randomart of the four fingerprints in random order:

        [ ]  [ ]
        
        [ ]  [ ]
        
        =none=

   Under the fingerprints, a „none of the above“ button is displayed.
   1. User clicks „none of the above“
   2. Client responds that the key may have been tampered with during
      the transfer and offers to
      - try again (full transfer)
      - manually compare fingerprints
         - Still different: Try again or abort (check for MitM)
         - The same: Proceed with signing.
5. User clicks on the image that manages the server’s.
  1. Wrong Key, client reponds: „This is not the key I received. Here,
     try to compare again:“ and shows the chosen randomart
  2. User responds:
     - „But I’m sure it’s the same“ ⇒ Man in the Middle
     - „You are right.“ ⇒ Try again (with different fakes)
6. The keys match, proceed with signing.

There is a very slight chance the key has been tampered with and the
user selects the tampered fingerprint by error. How to prevent that
and is that even possible?
