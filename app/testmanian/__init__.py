from time import sleep
from datetime import datetime
from httpwrapper import HttpReq
from config import base_dir, logger
import os
import re
import html
import pickle


class TestManian(HttpReq):
    BASE_URL = 'https://www.tesmanian.com/'
    RE_SITEMAP_BLOG_SITEMAP_LINK = r'<loc>(https:\/\/www.tesmanian.com\/sitemap_blogs.*?\.xml)<\/loc>'
    RE_SITEMAP_BLOG_LINK_AND_TITLE = r"<url>.*?<loc>(.*?)<\/loc>.*?<image:title>(.*?)<\/image:title>.*?</url"

    def __init__(self, config):
        super().__init__(useragent_file=config['pathes']['useragent'])
        self.api_token = config['alerts']['telegram']['token']
        self.chat_id = config['alerts']['telegram']['chatID']
        self.session_file = os.path.join(base_dir, 'testmanian.bin')
        self.user = config['account']['user']
        self.password =config['account']['password']
     #    self.data_dir = mkdir_p(os.path.join(base_dir, 'data'))

    def load_session(self):
        session_data = set()
        try:
            with open(self.session_file, 'rb') as f:
                session_data = pickle.load(f)
        except Exception as exc:
            msg = f'{self.__class__.__name__} load_session  Exception: {exc}'
            logger.error(msg)
        finally:
            return session_data

    def save_session(self, session_data):
        result = False
        try:
            with open(self.session_file, 'wb') as f:
                pickle.dump(session_data, f)
            result = True
        except Exception as exc:
            msg = f'{self.__class__.__name__} save_session  Exception: {exc}'
            logger.error(msg)
        finally:
            return result

    def get_sitemap(self, sitemap_url):
        sitemap_data = ''
        try:
            q_res, text_data, _, _ = self.req_get(url=sitemap_url)
            if q_res:
                sitemap_data = text_data
        except Exception as exc:
            msg = f'{self.__class__.__name__} get_sitemap  Exception: {exc}'
            logger.error(msg)
        finally:
            return sitemap_data

    def get_info_from_sitemap(self, regex, xml_data):
        data = []
        try:
            if xml_data:
                matches = re.finditer(regex, xml_data, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                for match in matches:
                    item = []
                    for subgroup in match.groups():
                        item.append(subgroup)
                    data.append(item)
        except Exception as exc:
            msg = f'{self.__class__.__name__} get_blogs_links_from_sitemap  Exception: {exc}'
            logger.error(msg)
        finally:
            return data

    def telegram_alert(self, msg):
        sent = False
        try:
            url = f'https://api.telegram.org/bot{self.api_token}/sendMessage'
            sent, text_data, json_data, _ = self.req_post(url=url, json_data={'chat_id': self.chat_id, 'text': msg})
            if not sent and json_data.get('error_code') == 429:
                timeout = json_data.get('parameters',{}).get('retry_after', 0)
                logger.info(f"Telegram timeout {timeout}")
                sleep(timeout)
        except Exception as exc:
            msg = f'{self.__class__.__name__} telegram_alert  Exception: {exc}'
            logger.error(msg)
        finally:
            sleep(0.2)
            return sent

    def run(self, timeout=1):
        while True:
            try:
                new_cnt = 0
                old_cnt = 0
                logger.info(f"Now {datetime.utcnow()}")
                session_data = self.load_session()
                sitemap = self.get_sitemap(sitemap_url=TestManian.BASE_URL+'sitemap.xml')
                blogs = self.get_info_from_sitemap(regex=TestManian.RE_SITEMAP_BLOG_SITEMAP_LINK, xml_data=sitemap)
                for blog in blogs:
                    sitemap_blog = self.get_sitemap(sitemap_url=blog[0])
                    if sitemap_blog:
                        for blog_index, blog_data in enumerate(self.get_info_from_sitemap(regex=TestManian.RE_SITEMAP_BLOG_LINK_AND_TITLE, xml_data=sitemap_blog), 1):
                            if blog_data[0].strip().lower() not in session_data:
                                logger.info(f"[{blog_index}] NEW!: URL {blog_data[0]} Title: {blog_data[1]}")
                                self.telegram_alert(f"URL {blog_data[0]} \nTitle: {html.unescape(blog_data[1])}")
                                session_data.add(blog_data[0].strip().lower())
                                new_cnt += 1
                            else:
                                logger.info(f"[{blog_index}] OLD!: URL {blog_data[0]} Title: {blog_data[1]}")
                                old_cnt += 1
                total_msg = f"\nStat: new - {new_cnt} old - {old_cnt}"
                logger.info(total_msg)
                self.telegram_alert(total_msg)
            except Exception as exc:
                msg = f'{self.__class__.__name__} run  Exception: {exc}'
                logger.error(msg)
            finally:
                self.save_session(session_data)
            logger.info(f"Sleeping for {timeout} sec...")
            sleep(timeout)
