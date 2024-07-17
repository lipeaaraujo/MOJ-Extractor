# MOJ Contest Data Extractor

this script extracts data from the CD-MOJ (Contest Driven Meta Online Judge) platform and saves it to a markdown file.

you can install the required modules using pip:

```bash
pip install requests -r requirements.txt
```
## Usage

1. clone this repository:
```bash
git clone https://github.com/lipeaaraujo/MOJ-Extractor.git
```

2. run the script with the required arguments:
```bash
python script.py <contest_url> --login <username> --password <password>
```
### Arguments
- `contest_url:` the URL of the contest page on the MOJ platform
- `--login:` your contest username.
- `--password:` your contest password.

## Output

this script will create a file named `contest.md` in the current directory, containing the contest title, description, and problems.

## Notes
- ensure that the provided URL is a valid contest page on the MOJ platform.
- your credentials are only used for loggin in to the MOJ platform and are not stored or shared