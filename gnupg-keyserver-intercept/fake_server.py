#!/usr/bin/env python3
import http.server as serv
import urllib.parse as parse

class HKPHTTPRequestHandler(serv.BaseHTTPRequestHandler):
    def do_GET(self):
        # query = parse.parse_qs(p.urlparse(self.path).query)
        # query['search']
        self.send_header('Content-Type', 'application/pgp-keys')
        self.end_headers()
        self.wfile.write(bad_key.encode())
        

bad_key = """
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v2

mI0EU/OlxQEEALh7BxkWhmG0l3H+Lhrj3OkeETt1Wj3Nd22ZRb1zUr5VyEdYWwge
+ItpAhYaEKUcrpW9+QAUHF+N6mLSqPhQVDX74zkeFxYZgOnWUoXEmrSrhQlxNhX1
BswWd2otr0ljY68cihPrs5IPyyy+Hyxf6cA6qy488AoiXkB2KJ8HP6pRABEBAAG0
JUpvaG4gRG9lIChCYWQga2V5KSA8am9obkBleGFtcGxlLmNvbT6IuQQTAQIAIwUC
U/OlxQIbAwcLCQgHAwIBBhUIAgkKCwQWAgMBAh4BAheAAAoJEIwrB/CvJdHGoxAE
AJ8vQLrUCloaV1PjwAs7bP552UbUQ42sGmkyrtR/DemDprRkyJJ8nflFcVAIeChi
2z3A8Mvmhf7ZxgPKYcq26SgmZTpUmYUduGNyQXPtrn0DFjfF/FkEpuPy0ntDXW8u
4LuFH1u4B46BPTBCmfOFnhf+Co5Zcq/K1+wbAGcuwIqguI0EU/OlxQEEALNTfX1a
cRPhvN9aiWk6ws1xbrdNJyaHHp2sxf2M7r76Pc6V2MFoO+3Wxjkng9QzNJRVMkyB
0Pvg+wHhIkVnhEvIQTclcwdYs0vsDqGlOQNd8GT+mxZG1VcgEGX6kh9cHr5gd8Rg
nMrf715j9cYvUH8ZEAzJEXadD3AC2b6V9gRTABEBAAGInwQYAQIACQUCU/OlxQIb
DAAKCRCMKwfwryXRxkkiA/wMr1JNuZ2t3PMOct0Q2Pn7XyUc+9LfEwlXKWYT8Gkp
oWxh08T3/LjsFklOS4LldQkApj8lY5vG7oxAIgmUUOdGTO/o7G8rgDyHIEOscFq0
P4Wt2vcYVpa+aFIFJI2hCVOmdXnwGjN9iI4nGrYItXZX0052U63+1S3xFi3cn7wd
8g==
=lwoq
-----END PGP PUBLIC KEY BLOCK-----
"""
        
if __name__ == "__main__":
    server_address = ('localhost', 11371)
    httpd = serv.HTTPServer(server_address, HKPHTTPRequestHandler)
    httpd.serve_forever()

