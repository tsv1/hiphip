import json
from collections import OrderedDict

import requests


class Response(requests.Response):

    def __repr__(self):
        r = "{method} {url}\n".format(method=self.request.method, url=self.request.url)

        request_content_type = self.request.headers.get("content-type", "text/plain").lower()
        if request_content_type.startswith("text/") or request_content_type.endswith("/text"):
            r += str(self.request.body)
        elif request_content_type.startswith("application/json"):
            try:
                request_text = json.loads(self.request.body)
            except:
                request_text = 'Raw: {}'.format(self.request.body)
            r += json.dumps(request_text, sort_keys=True, ensure_ascii=False, indent=2)
        r += "\n\n"
        
        r += "HTTP/1.1 {status}\n".format(status=self.status_code)
        for key, value in OrderedDict(sorted(self.headers.items())).items():
            r += "{key}: {value}\n".format(key=key, value=value)

        content_type = self.headers.get("content-type", "text/plain").lower()
        if content_type.startswith("text/") or content_type.endswith("/text"):
            r += "\n" + str(self.text)
        elif content_type.startswith("application/json"):
            try:
                text = json.loads(self.text)
            except:
                text = ""
            r += "\n" + json.dumps(text, sort_keys=True, ensure_ascii=False, indent=2)

        return r
