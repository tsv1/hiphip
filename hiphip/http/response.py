import json
from collections import OrderedDict

import requests


class Response(requests.Response):
    def __repr__(self):
        def _log_body(headers, body):
            r = ""

            request_content_type = headers.get("content-type", "text/plain").lower()
            if request_content_type.startswith("text/"):
                r += str(body)
            elif request_content_type.startswith("application/json"):
                try:
                    request_text = json.loads(body)
                except:
                    r += "Non-parsed json: {}".format(str(body))
                else:
                    r += json.dumps(request_text, sort_keys=True, ensure_ascii=False, indent=4)
            else:
                r += str(body)

            return r

        r = "{method} {url}\n".format(method=self.request.method, url=self.request.url)

        r += _log_resp(self.request.headers, self.request.body)
        r += "\n\n"

        r += "HTTP/1.1 {status}\n".format(status=self.status_code)
        for key, value in OrderedDict(sorted(self.headers.items())).items():
            r += "{key}: {value}\n".format(key=key, value=value)

        r += _log_resp(self.headers, self.text)

        return r
