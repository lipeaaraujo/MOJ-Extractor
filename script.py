import argparse
import requests
from bs4 import BeautifulSoup

# configuring argparser
parser = argparse.ArgumentParser(description="extract contest data from moj")
parser.add_argument("url", type=str, help="url from contest")
parser.add_argument("--login", type=str, required=True, help="contest username")
parser.add_argument("--password", type=str, required=True, help="contest password")
args = parser.parse_args()

def derive_login_url(contest_url):
  return contest_url.replace("contest.sh", "login.sh")

def init_session():
  # login url and data
  login_url = derive_login_url(args.url)
  login_data = {
    'login': (None, args.login),
    'senha': (None, args.password)
  }
  
  # make login HTTP request
  with requests.Session() as session:
    login_response = session.post(login_url, files=login_data)
    
    if login_response.status_code == 200:
      # extract cookies from login response
      cookie_script = BeautifulSoup(login_response.content, 'html.parser').find('script').string
      login_cookie = cookie_script.split('document.cookie="login=')[1].split(';')[0]
      hash_cookie = cookie_script.split('document.cookie="hash=')[1].split(';')[0]
      
      # configure cookies in the session
      session.cookies.set('login', login_cookie)
      session.cookies.set('hash', hash_cookie)
          
      request_contest(session)
    else:
      print(f'error on login: {login_response.status_code}')
  
def request_contest(session):
  # use url and get HTTP response
  url = args.url
  response = session.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())

  else:
    print(f'error on getting response from url: {response.status_code}')
    
init_session()
