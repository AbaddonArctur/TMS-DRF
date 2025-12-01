from django.urls import reverse


def obtain_access_token(client, username, password):
    resp = client.post(
        reverse("token_obtain_pair"),
        {"username": username, "password": password},
        format="json",
    )

    if isinstance(resp.data, dict) and resp.data.get("access"):
        return resp.data["access"]

    ck = resp.cookies.get("access")
    if ck:
        return ck.value

    raise RuntimeError(
        f"Token obtain failed: status={resp.status_code}, data={resp.data}"
    )
