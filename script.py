import argparse
import requests
from bs4 import BeautifulSoup

# configuring argparser to handle command-line arguments
parser = argparse.ArgumentParser(description="extract contest data from moj")
parser.add_argument("url", type=str, help="url from contest")
parser.add_argument("--login", type=str, required=True, help="contest username")
parser.add_argument("--password", type=str, required=True, help="contest password")
args = parser.parse_args()

def derive_login_url(contest_url):
  # Derives the login URL form the contest URL
  return contest_url.replace("contest.sh", "login.sh")

def init_login_session():
  # Initialize a session and login
  login_url = derive_login_url(args.url)
  login_data = {
    'login': (None, args.login),
    'senha': (None, args.password)
  }
  
  with requests.Session() as session:
    # make login HTTP request
    login_response = session.post(login_url, files=login_data)
    
    if login_response.status_code == 200:
      # extract cookies from login response
      cookie_script = BeautifulSoup(login_response.content, 'html.parser').find('script').string
      login_cookie = cookie_script.split('document.cookie="login=')[1].split(';')[0]
      hash_cookie = cookie_script.split('document.cookie="hash=')[1].split(';')[0]
      
      # set cookies in the session
      session.cookies.set('login', login_cookie)
      session.cookies.set('hash', hash_cookie)
        
      # request the contest data
      request_contest(session)
    else:
      print(f'error on login: {login_response.status_code}')

def parse_contest(soup):
  # Parse the contest HTML content and save to a markdown file
  content_div = soup.find(id="text")
  problem_ulist = content_div.find('ul')
  problems = problem_ulist.find_all('li')

  with open('contest.md', 'w') as output:
    # write contest title and description
    output.write('# (Contest title)\n\n')
    output.write('(description here)\n\n')
    
    # write each problem to the output file
    for problem in problems:
      letter = problem.find('b').text.strip()
      title = problem.get_text().split('-')[1].strip()
      link = problem.find('a')['href']
      
      # format each problem
      formatted_problem = f'## {letter} - {title}\n\n{link}\n\n'
      output.write(formatted_problem)
      
      # placeholder for solution
      output.write("- **[Solution]()**\n\n")
      
def request_contest(session):
  # Request the contest page using the session with login cookies
  url = args.url
  response = session.get(url)

  if response.status_code == 200:
    # parse the contest page content
    soup = BeautifulSoup(response.content, 'html.parser')
    parse_contest(soup)

  else:
    print(f'error on getting response from url: {response.status_code}')

# Initialize login session and start the process
init_login_session()
