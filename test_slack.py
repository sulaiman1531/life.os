import urllib.request
import json
import ssl

token = "xoxe.xoxp-1-Mi0yLTExNjU5NDk0NDg4Mjg5LTExNjQyMjA2NzQxNzk5LTExNjg1OTE1NDM5MzI4LTExNjYxMjgyOTIyNjkyLTk5Yzk5MWEyNzNlMDliZjRkMDk0ODIyZTgxOGRjZjMwZjc1OTM3NGI5Mjc0OThkMTgwNDQ1YTMyYmI4NTRiZDA"

try:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        "https://slack.com/api/search.messages?query=to:me&sort=timestamp&sort_dir=desc&count=5",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req, timeout=5, context=context) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print("Error:", e)
