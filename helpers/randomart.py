"""Draw an ASCII-Art representing the fingerprint so human brain can
profit from its built-in pattern recognition ability.
This technique is called "random art" and can be found in some
scientific publications like this original paper:

"Hash Visualization: a New Technique to improve Real-World Security",
Perrig A. and Song D., 1999, International Workshop on Cryptographic
Techniques and E-Commerce (CrypTEC '99)
sparrow.ece.cmu.edu/~adrian/projects/validation/validation.pdf

The subject came up in a talk by Dan Kaminsky, too.

If you see the picture is different, the key is different.
If the picture looks the same, you still know nothing.

The algorithm used here is a worm crawling over a discrete plane,
leaving a trace (augmenting the field) everywhere it goes.
Movement is taken from the fingerprint 2bit-wise.  Bumping into walls
makes the respective movement vector be ignored for this turn.
Graphs are not unambiguous, because circles in graphs can be
walked in either direction.

Transcribed from OpenSSHs key.c (function key_fingerprint_randomart)
"""


class Randomart:
    def __init__(self, fingerprint, size):
        """Randomart representation of hex fingerprints

        :param fingerprint: Hexstring, length multiples of bytes
        :param size: (width, height), must be uneven and >2

        """

        # Chars to be used after each other every time the worm
        # intersects with itself. Matter of taste.
        self.AUGMENTATION_STRING = " .o+=*BOX@%&#/^SE"
        self.fingerprint = fingerprint
        self.width, self.height = size

    def _key_fingerprint_walk(self):
        """Return a matrix representation of the worm/drunken bishop algorithm

        :rtype: (matrix, startpoint (x,y), endpoint (x,y))
        """
        width, height = self.width, self.height
        if len(self.fingerprint)%2 != 0:
            raise ValueError(
                "Fingerprint must align to bytes (length even)")
        if width%2 == 0 or height%2 == 0 or width < 3 or height < 3:
            raise ValueError("One of size >3 and/or uneven")

        # raw fingerprint
        fp_bytearray = bytearray.fromhex(self.fingerprint)
        # zero matrix h×w
        field = [[0]*width for i in range(height)]
        # coordinates of walk
        start = int(width/2), int(height/2)
        x, y = start

        # process raw key
        for byte in fp_bytearray:
            # each byte conveys four 2-bit move commands (pairs)
            for pair in range(4):
                # evaluate 2 bit, rest is shifted later
                x += 1 if (byte & 0x1) else -1
                y += 1 if (byte & 0x2) else -1

                # assure we are still in bounds
                x = max(x, 0)
                y = max(y, 0)
                x = min(x, width - 1)
                y = min(y, height - 1)

                # augment the field
                field[y][x] += 1
                byte = byte >> 2

                ## steps
                # for l in field:
                #     print(l)
                # print("")

        end = x, y
        return field, start, end

    def get_matrix(self):
        """Get the matrix representation."""
        return self._key_fingerprint_walk()

    def to_ascii(self):
        """Returns an ascii representation."""
        field, start, end = self.get_matrix()
        # Maximum value that can be represented with the augstring
        maxval = len(self.AUGMENTATION_STRING) - 3

        upper_border = "+" + "-" * (self.width) + "+"
        lower_border = upper_border

        field_cut = []
        for row in field:
            # high cut values exceeding available symbols
            field_cut.append([min(v, maxval) for v in row])

        # Mark starting point and end points
        sx, sy = start
        ex, ey = end
        field_cut[sy][sx] = maxval + 1
        field_cut[ey][ex] = maxval + 2

        ascii_field = []
        for row in field_cut:
            # replace with ascii
            ascii_field.append(
                "|{}|".format(
                    "".join([self.AUGMENTATION_STRING[v]
                             for v in row])))

        return "{}\n{}\n{}\n".format(upper_border,
                                     "\n".join(ascii_field),
                                     lower_border)
