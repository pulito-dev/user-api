from auth0.management import Auth0
from auth0.authentication import GetToken
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier

domain = "pulito.eu.auth0.com"
jwks_url = f"https://{domain}/.well-known/jwks.json"
api_url = f"https://{domain}/api/v2/"
client_id = "Ta5xPVRrIvVz6Ktk1d1aNIMsy1ntWwEX"
client_secret = "vsBFHAfPrAF4VoyR0VzQ-qZNlmglwKQIWW9B4ZTeYXpHGGj0mNSugYVx7wapuVaU"

get_token = GetToken(
    domain=domain,
    client_id=client_id,
    client_secret=client_secret
)

token = get_token.client_credentials(api_url)

mgmt_api_token = token["access_token"]

auth0 = Auth0(domain, mgmt_api_token)

# get all users
# print(auth0.users.list())

# get user id token
user_token = get_token.login(
scope="openid profile",
username="test@test.com",
password="testtest12.",
realm="Username-Password-Authentication"
)
print(user_token["id_token"])

# token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBNQnozYU1kV3lzR2NNMjNZUXNFWiJ9.eyJuaWNrbmFtZSI6InRlc3QiLCJuYW1lIjoidGVzdEB0ZXN0LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci9iNjQyYjQyMTdiMzRiMWU4ZDNiZDkxNWZjNjVjNDQ1Mj9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnRlLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDI0LTEyLTA0VDEzOjM4OjU3LjU0NFoiLCJpc3MiOiJodHRwczovL3B1bGl0by5ldS5hdXRoMC5jb20vIiwiYXVkIjoiVGE1eFBWUnJJdlZ6Nkt0azFkMWFOSU1zeTFudFd3RVgiLCJpYXQiOjE3MzMzMTk1MzcsImV4cCI6MTczMzM1NTUzNywic3ViIjoiYXV0aDB8Njc0ZmFhZjJiYTBhMzM3MjhmMzZlOWZjIn0.1_oBzoIDcMi5ViyvQBspgxQmPhRMP97zCgyNVeOZ3Dc-x5zKb9lTEqcbEKDVbyDZEeDEKCtCQgNx_Yf6kzZ9lRMktyfAGTBNzXbzl21YS6Ryt_5SUVC9eEwSP4gLGvLY5fyLMUzwGCwctrUNYRHXUoks_coC9NaoGbyGHoL2mwEwQwR-sYzl8V7iKDhdO3RoNIgLLEy46bK1sCZXTQ5lkmjTdvhzIeV81b5-vBSAWdl368vTFHRMM1hh8Unm2_hTtEIVwr9KmleKXdjhyI_b1L3_nib3YS8TUQnUQ36PSxFjMLmxbC2nigtPVGUGaxadWPnStesgXf6-2g97AWTd7g"
# exp_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBNQnozYU1kV3lzR2NNMjNZUXNFWiJ9.eyJuaWNrbmFtZSI6InRlc3QiLCJuYW1lIjoidGVzdEB0ZXN0LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci9iNjQyYjQyMTdiMzRiMWU4ZDNiZDkxNWZjNjVjNDQ1Mj9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnRlLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDI0LTEyLTA0VDAxOjI0OjU1LjA0MloiLCJpc3MiOiJodHRwczovL3B1bGl0by5ldS5hdXRoMC5jb20vIiwiYXVkIjoiVGE1eFBWUnJJdlZ6Nkt0azFkMWFOSU1zeTFudFd3RVgiLCJpYXQiOjE3MzMyNzU0OTUsImV4cCI6MTczMzMxMTQ5NSwic3ViIjoiYXV0aDB8Njc0ZmFhZjJiYTBhMzM3MjhmMzZlOWZjIn0.0USDtdHABbzIV7MjKUzjVan1ntYZ_PswaWh-E0i2YLgZ_5FMMfwJbqOxwWmVmK4kcrMwT-_BP05Yn3ePD4PdQHhBXxs37R7bTFCGQudT2C53n_0Sn8tGm2bVXRnxqzbI9MZ6LO7k1P9EVzZ5RNK616Do43K1Ut0p6H_XEjHTKOEcZ_0Wqu2c7FIoRSx8zznLihzAmEVJAosRnz2YFuuTcvFCH7MzbyAlRxSj5ImI7EDj6Mhv6pCNXbXZSjv5Pj015vmvCMQOSW03EoWcMnGc7zTuw8Q0_SvlviFW6cs2ZFiwpWm2uV1GjHA0-prr73ihZ7UOFr-PJ-HnRfg-wOKDsg"

# verify token signature and expiry
# sv = AsymmetricSignatureVerifier(jwks_url)
# tv = TokenVerifier(sv, f"https://{domain}/", audience=client_id)

# res = tv.verify(token)
# print(res)
