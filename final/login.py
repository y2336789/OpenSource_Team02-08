# parser.py
import requests
from bs4 import BeautifulSoup as bs
import webbrowser
import menu1
import menu2
import loginform
import PySpaceShip
import tengaii

#헤더 정보입니다.
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
headers = {'User-Agent':'Chrome/66.0.3359.181'}
headers = {'User-Agent':'Mozilla/5.0', 'referer' : 'http://www.naver.com'}

data = {
    'username': ' ',
    'password': ' '
}

update1_data = {
	'score_one': '0',
}

update2_data = {
	'score_two': '0',
}

update3_data = {
	'score_three': '0',
}

URL = 'http://noriaki.pythonanywhere.com/'
signup_URL = 'http://noriaki.pythonanywhere.com/signup/'
update1_URL = 'http://noriaki.pythonanywhere.com/update1/'
update2_URL = 'http://noriaki.pythonanywhere.com/update2/'
update3_URL = 'http://noriaki.pythonanywhere.com/update3/'

def update1(score_one):
	global update1_data
	update1_page = s.get(update1_URL)
	html = update1_page.text
	soup = bs(html, 'html.parser')
	csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})
	update1_data = {**update1_data, **{'csrfmiddlewaretoken': csrf['value']}}
	update1_data['score_one'] = score_one
	update1_req = s.post(update1_URL, data=update1_data, headers = headers)
	print(update1_req)

def update2(score_two):
	global update2_data
	update2_page = s.get(update2_URL)
	html = update2_page.text
	soup = bs(html, 'html.parser')
	csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})
	update2_data = {**update2_data, **{'csrfmiddlewaretoken': csrf['value']}}
	update2_data['score_two'] = score_two
	update2_req = s.post(update2_URL, data=update2_data, headers = headers)
	print(update2_req)

def update3(score_three):
	global update3_data
	update3_page = s.get(update3_URL)
	html = update3_page.text
	soup = bs(html, 'html.parser')
	csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})
	update3_data = {**update3_data, **{'csrfmiddlewaretoken': csrf['value']}}
	update3_data['score_three'] = score_three
	update3_req = s.post(update3_URL, data=update3_data, headers = headers)
	print(update3_req)

def PrintInfo():
    post_one = s.get(URL)
    soup = bs(post_one.text, 'html.parser')
    score1 = soup.select('#home-section > div.site-section > div > div:nth-child(2) > div:nth-child(1) > div')
    score2 = soup.select('#home-section > div.site-section > div > div:nth-child(2) > div:nth-child(2) > div')
    #score3 = soup.select('#home-section > div.site-section > div > div:nth-child(2) > div:nth-child(3) > div')

    for title in score1:
        print(title.find('h3').get_text())
        print(title.find('h2').get_text())

    for title in score2:
        print(title.find('h3').get_text())
        print(title.find('h2').get_text())
'''
    for title in score3:
        print(title.find('h3').get_text())
        print(title.find('h2').get_text())
'''

def Greeting():
    post_one = s.get(URL)
    soup = bs(post_one.text, 'html.parser')
    id = soup.select('#home-section > div.ftco-blocks-cover-1 > div > div > div > div.col-md-5.mt-5.pt-5 > h1')
    print(id[0].text+'님, 환영합니다!')

def ShowGlory():
    post_one = s.get('http://noriaki.pythonanywhere.com/glory/')
    soup = bs(post_one.text, 'html.parser')
    glory1 = soup.select('#home-section > div.site-section > div > div:nth-child(2) > div:nth-child(1) > div')
    glory2 = soup.select('#home-section > div.site-section > div > div:nth-child(2) > div:nth-child(2) > div')
    #glory3 = soup.select('#home-section > div.site-section > div > div:nth-child(2) > div:nth-child(3) > div')

    print('<명예의 전당>')
    for title in glory1:
        for sub_title in title.find_all('h2'):
            print(sub_title.get_text())
        print(title.find('h3').get_text())

    for title in glory2:
        for sub_title in title.find_all('h2'):
            print(sub_title.get_text())
        print(title.find('h3').get_text())
'''
    for title in glory3:
        for sub_title in title.find_all('h2'):
            print(sub_title.get_text())
        print(title.find('h3').get_text())
'''

def login(str1, str2):
    global data
    data['username']=str1
    data['password']=str2

    first_page = s.get(URL)
    html = first_page.text
    soup = bs(html, 'html.parser')
    csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'}) # input태그 중에서 name이 _csrf인 것을 찾습니다.
    #print(csrf['value']) # 위에서 찾은 태그의 value를 가져옵니다.

    # 이제 LOGIN_INFO에 csrf값을 넣어줍시다.
    # (p.s.)Python3에서 두 dict를 합치는 방법은 {**dict1, **dict2} 으로 dict들을 unpacking하는 것입니다.
    data = {**data, **{'csrfmiddlewaretoken': csrf['value']}}

    #로그인
    login_req = s.post(URL, data=data, headers = headers)

    #로그인 검사
    post_one = s.get(URL)
    soup = bs(post_one.text, 'html.parser')
    info = soup.select('#home-section > div.ftco-blocks-cover-1 > div > div > div > div.col-md-5.mt-5.pt-5 > p')
    if info[0].text == '좌측에 정보를 입력해주세요.':
        print('아이디 또는 비밀번호가 일치하지 않습니다. 정확한 정보를 입력해주세요.') #로그인 실패 메시지
        return False
    else:
        return True

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:
    first_work=menu1.main()
    while True:
        if first_work==1:
            Info = loginform.input_string()
            value=login(Info[0],Info[1])
            if value:
                Greeting()
                break
        elif first_work==2:
            webbrowser.open(signup_URL)
            first_work=menu1.main()
        else:
            print('올바른 작업을 선택해주세요.')

    # -- 여기서부터는 로그인이 된 세션이 유지--
    while True:
        #작업 설정
        work = menu2.main()
        if work==1:
            #init_score = 0
            value = 0
            while value==0:
                score_list = PySpaceShip.game1()
                update1(score_list[1])
                if score_list[0]=='0':
                    PySpaceShip.score = score_list[1]
                elif score_list[0]=='1':
                    PySpaceShip.score = 0
                    value=1

        elif work==2:
            value = 0
            while value==0:
                score_list = tengaii.game2()
                update3(score_list[1])
                if score_list[0]=='0':
                    tengaii.s_score = score_list[1]
                elif score_list[0]=='1':
                    tengaii.s_score = 0
                    value=1
        elif work==5:
            break
        '''
        work = int(input('=============\n작업을 선택해주세요. \n1. 명예의 전당 \n2. 새로운 게임 \n3. 내 기록 보기 \n4. 로그아웃\n5. 끝내기\n=============\n'))
        if work==5: #끝내기
            break
        elif work==4: #재로그인
            logout_req = s.get('http://noriaki.pythonanywhere.com/logout/') #로그아웃 페이지로 이동하면 곧바로 로그아웃이 된다.
            value = input('로그아웃 되었습니다!\n재로그인 하시겠습니까? (y/n)')
            if value=='y':
                #login()
                pass
            else:
                break
        elif work==3: #
            print('=== 나의 최고 점수 ===')
            PrintInfo()

        #업데이트
        elif work==2:
            game_order = int(input('게임을 선택하세요! \n1. 운석피하기\n2. 텐가이\n(1,2)'))
            if game_order==1:
                value = int(input('운석피하기의 새로운 점수를 입력해주세요.'))
                update1(value)
            elif game_order==2:
                value = int(input('텐가이의 새로운 점수를 입력해주세요.'))
                update3(value)

            #업데이트된 정보 출력
            print('=== 업데이트된 점수 ===')
            PrintInfo()

        elif work==1:
            ShowGlory()

        else:
            print('올바른 작업을 선택해주세요.')
        '''

    print('게임을 종료합니다.')
