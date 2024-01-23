from mitmproxy.http import HTTPFlow,Response

class ResourceLoader:
    def __init__(self):
        self.num = 0

    def request(self, flow:HTTPFlow):
        if "client.wasm" in flow.request.url:
            flow.response = Response.make(
                200,
                open("cli.wasm","rb").read(),
                {
                    "Content-Type": "application/wasm",
                    "access-control-allow-methods":"GET, HEAD, OPTIONS",
                    "access-control-allow-origin":"*",
                    "access-control-max-age":"86400"
                },
            )


addons = [ResourceLoader()]