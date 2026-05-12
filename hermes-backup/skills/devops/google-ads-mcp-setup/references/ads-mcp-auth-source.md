# google-ads-mcp Authentication Source Code Evidence

## Source A: `ads_mcp/utils.py` — PyPI Version (STALE)

The PyPI package (`google-ads-mcp` from pip) uses `google.auth.default()` only — NO OAuth support:

```python
def _create_credentials() -> google.auth.credentials.Credentials:
    """Returns Application Default Credentials with read-only scope."""
    (credentials, _) = google.auth.default(scopes=[_READ_ONLY_ADS_SCOPE])
    return credentials

def _get_developer_token() -> str:
    dev_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
    if dev_token is None:
        raise ValueError("GOOGLE_ADS_DEVELOPER_TOKEN environment variable not set.")
    return dev_token

def _get_login_customer_id() -> str:
    return os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")

def _get_googleads_client() -> GoogleAdsClient:
    # Use this line if you have a google-ads.yaml file
    # client = GoogleAdsClient.load_from_storage()
    client = GoogleAdsClient(
        credentials=_create_credentials(),
        developer_token=_get_developer_token(),
        login_customer_id=_get_login_customer_id(),
    )
    return client
```

## Source B: `ads_mcp/utils.py` — GitHub Main (commit `0d15712`, 2026-05-11)

The GitHub version adds **FastMCP OAuth token injection** before the ADC fallback:

```python
_ADS_SCOPE = "https://www.googleapis.com/auth/adwords"

def _create_credentials() -> google.auth.credentials.Credentials:
    """Returns Application Default Credentials with the Google Ads scope,
    or the FastMCP token if found."""
    from fastmcp.server.dependencies import get_access_token
    from google.oauth2.credentials import Credentials

    token_obj = get_access_token()
    if token_obj and token_obj.token:
        # Create credentials using the access token provided by FastMCP
        return Credentials(token=token_obj.token)

    credentials, _ = google.auth.default(scopes=[_ADS_SCOPE])
    return credentials

def _get_developer_token() -> str:
    dev_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
    if dev_token is None:
        raise ValueError("GOOGLE_ADS_DEVELOPER_TOKEN environment variable not set.")
    return dev_token

def _get_login_customer_id() -> str | None:
    return os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")

def _get_googleads_client() -> GoogleAdsClient:
    args = {
        "credentials": _create_credentials(),
        "developer_token": _get_developer_token(),
        "use_proto_plus": True,
    }
    login_customer_id = _get_login_customer_id()
    if login_customer_id:
        args["login_customer_id"] = login_customer_id
    client = GoogleAdsClient(**args)
    return client
```

## Key Differences

| Aspect | PyPI Version | GitHub Version |
|--------|-------------|----------------|
| Auth mechanism | ADC only | FastMCP OAuth → ADC fallback |
| OAuth env vars | Not read | `GOOGLE_ADS_MCP_OAUTH_CLIENT_ID`, `GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET` |
| Transport | stdio | stdio (ADC) / HTTP (OAuth) |
| `use_proto_plus` | Not set | `True` |
| API version | v21 | v24 |
| Install command | `uvx google-ads-mcp` | `uvx --from git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp` |

## Error Signatures

**ADC not configured (both versions):**
```
google.auth.exceptions.DefaultCredentialsError: Your default credentials were not found.
To set up Application Default Credentials, see https://cloud.google.com/docs/authentication/external/set-up-adc
```

**Hermes MCP CancelledError (PyPI version with no ADC):**
```
WARNING tools.mcp_tool: MCP server 'google-ads-mcp' failed initial connection after 3 attempts, giving up: unhandled errors in a TaskGroup (1 sub-exception)
```

## Environment Variables Actually Read

| Variable | PyPI | GitHub | Notes |
|----------|------|--------|-------|
| `GOOGLE_APPLICATION_CREDENTIALS` | ✅ ADC | ✅ fallback ADC | Service account JSON path |
| `GOOGLE_ADS_DEVELOPER_TOKEN` | ✅ | ✅ | Developer token |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | ✅ | ✅ | MCC account ID |
| `GOOGLE_ADS_MCP_OAUTH_CLIENT_ID` | ❌ | ✅ OAuth | FastMCP OAuth (B path) |
| `GOOGLE_ADS_MCP_OAUTH_CLIENT_SECRET` | ❌ | ✅ OAuth | FastMCP OAuth (B path) |
| `GOOGLE_ADS_MCP_BASE_URL` | ❌ | ✅ OAuth | FastMCP HTTP server URL |
| `GOOGLE_ADS_CLIENT_ID` | ❌ | ❌ | NOT read by either version |
| `GOOGLE_ADS_CLIENT_SECRET` | ❌ | ❌ | NOT read by either version |
