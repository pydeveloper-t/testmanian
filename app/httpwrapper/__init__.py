from useragents import UA
from config import CONFIG, logger
import requests

class HttpReq:
    def __init__(self, useragent_file):
        self.ua = UA(useragent_file)
        self.useragent = self.ua.get_random_useragent()
        self.headers = {'User-Agent': self.useragent}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def req_options(self, url, headers=None, params=None, cookies=None, useragent=None):
        q_res = False
        text_data = ''
        json_data = {}
        cookies_data = {}
        loc_headers = self.session.headers
        if headers:
            loc_headers.update(headers)
        if useragent is not None:
            if type(useragent) is bool and useragent:
                loc_headers.update({'User-Agent': self.ua.get_random_useragent()})
            elif type(useragent) is str and useragent:
                loc_headers.update({'User-Agent': useragent})
        try:
            with self.session as s:
                r = s.options(url, headers=loc_headers, params=params, cookies=cookies)
                if r.status_code >= 200 and r.status_code < 300:
                    q_res = True
                    for c in s.cookies:
                        cookies_data.update({c.name: c.value})
                    text_data = r.text
                    try:
                        json_data = r.json()
                    except:
                        pass
                else:
                    logger.error(f'[HTTP GET]  {r.status_code} {r.text}')
        except Exception as exc:
            msg = f'[HTTP OPTIONS] Exception: {exc}'
            logger.error(msg)
        finally:
            return q_res, text_data, json_data, cookies_data


    def req_get(self, url, headers=None, params=None, cookies=None, useragent=None):
        q_res = False
        text_data = ''
        json_data = {}
        cookies_data = {}
        loc_headers = self.session.headers
        if headers:
            loc_headers.update(headers)
        if useragent is not None:
            if type(useragent) is bool and useragent:
                loc_headers.update({'User-Agent': self.ua.get_random_useragent()})
            elif type(useragent) is str and useragent:
                loc_headers.update({'User-Agent': useragent})
        try:
            with self.session as s:
                r = s.get(url, headers=loc_headers, params=params, cookies=cookies)
                if r.status_code == 200:
                    q_res = True
                    for c in s.cookies:
                        cookies_data.update({c.name: c.value})
                    text_data = r.text
                    try:
                        json_data = r.json()
                    except:
                        pass
                else:
                    logger.error(f'[HTTP GET]  {r.status_code} {r.text}')
        except Exception as exc:
            msg = f'[HTTP GET] Exception: {exc}'
            logger.error(msg)
        finally:
            return q_res, text_data, json_data, cookies_data

    def req_post(self, url, json_data=None, data=None, headers=None, cookies=None, useragent=None):
        q_res = False
        text_data = ''
        local_json_data = {}
        local_cookies_data = {}
        loc_headers = self.session.headers
        if headers:
            loc_headers.update(headers)
        if useragent is not None:
            if type(useragent) is bool and useragent:
                loc_headers.update({'User-Agent': self.ua.get_random_useragent()})
            elif type(useragent) is str and useragent:
                loc_headers.update({'User-Agent': useragent})
        try:
            with self.session as s:
                if json_data:
                    r = s.post(url, json=json_data, headers=loc_headers, cookies=cookies)
                elif data:
                    r = s.post(url, data=data, headers=loc_headers, cookies=cookies)
                if r.status_code == 200:
                    q_res = True
                    for c in s.cookies:
                        local_cookies_data.update({c.name: c.value})
                    text_data = r.text
                    try:
                        local_json_data = r.json()
                    except:
                        pass
                else:
                    q_res = False
                    text_data = r.text
                    try:
                        local_json_data = r.json()
                    except:
                        pass
        except Exception as exc:
            msg = f'[HTTP POST] Exception: {exc}'
            logger.error(msg)
        finally:
            return q_res, text_data, local_json_data, local_cookies_data

