import re
import subprocess

import requests

from interface import UserInfo
from log import logger
from settings import DEFAULT_USER_AGENT, URL_FETCH_USER_INFO, PATH_SCRIPT_GET_ANTI_CONTENT, PATH_NODE


def preprocess_cookie(_cookie: str) -> str:
    return [i for i in re.split(r'\s', _cookie) if i][-1]


def verify_cookie_strict(cookie: str) -> UserInfo:
    """
    最重要的两个字段是 _nano_fp 和 SUB_PASS_ID
    """
    assert cookie, 'cookie不能为空！'
    assert not re.search(r'\s', cookie), 'cookie内不能有空！'
    
    try:
        anti_content = subprocess.Popen([PATH_NODE, PATH_SCRIPT_GET_ANTI_CONTENT, cookie], stdout=subprocess.PIPE,
                                        encoding='utf-8').stdout.read().strip()
    except Exception as e:
        print({"cookie": cookie, "path": PATH_SCRIPT_GET_ANTI_CONTENT, "error": e.__str__()})
        raise e
    
    data = {'crawlerInfo': anti_content}
    
    headers = {
        'anti-content': anti_content,
        'user_result-agent': DEFAULT_USER_AGENT,
        'COOKIE': cookie
    }
    # logger.info({"cookie": cookie, "anti-content": anti_content})
    try:
        res = requests.post(URL_FETCH_USER_INFO, data=data, headers=headers).json()  # type: dict
    except Exception as e:
        raise ValueError("登录失败", e)
    if not res.get("success"):
        logger.error(res)
        raise ValueError('登录失败：', res)
    logger.info('VERIFICATION OF COOKIE PASSED!')
    return res['result']


if __name__ == '__main__':
    cookie = '''// Semicolon separated Cookie File
// This file was generated by EditThisCookie
// Details: http://www.ietf.org/rfc/rfc2109.txt
// Example: http://www.tutorialspoint.com/javascript/javascript_cookies.htm
_a42=bdd210e2-64fd-45a8-8322-fbc952649bc3;_bee=QmYHLpZqatu7tlULci8DHBhRPcIVqfiB;_crr=QmYHLpZqatu7tlULci8DHBhRPcIVqfiB;_f77=e4a8701b-6ec3-4ad5-b99e-5b91f6a962e8;api_uid=rBRozWCVSc4r1kMSK4FXAg==;rcgk=QmYHLpZqatu7tlULci8DHBhRPcIVqfiB;rckk=QmYHLpZqatu7tlULci8DHBhRPcIVqfiB;ru1k=e4a8701b-6ec3-4ad5-b99e-5b91f6a962e8;ru2k=bdd210e2-64fd-45a8-8322-fbc952649bc3;_bee=IyctlSCGL1k8SVLI2bTMNCIh9EpeZLCr;_nano_fp=XpEalpUxnpXyXqToXo_2zmpGnwf0Lw56s1VNG1Uj;JSESSIONID=DBEEF23D1C6582A70A50192D861342E0;mms_b84d1838=120,3397,3432,1202,1203,1204,1205;PASS_ID=1-KQYAjOu8LLEznJln6MCzrfXeESwdCQBb2/zTup5ju6t0iyGtny/tl2TH+b27WX+U9NlzxqfciKJ44SDsNpKgng_506673970_93917892;x-visit-time=1620477578419;'''
    cookie = cookie.splitlines()[-1]
    print(verify_cookie_strict(cookie))
