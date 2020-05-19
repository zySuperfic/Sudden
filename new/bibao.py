
import requests
import json
# 创建会话
s = requests.session()

# 登录要请求的地址，
url = "http://ecshop.itsoso.cn/ECMobile/?url=/user/signin"
# 登录所需要的get参数
# 通过抓包的到需要传递的参数
data  = {'name':'stevebob','password':'3882547'}
# 通过抓包或chrome开发者工具分析得到登录的请求头信息,
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}


# 开始登录
r = s.post(url=url, data=data, headers=headers)
print(r.text)
