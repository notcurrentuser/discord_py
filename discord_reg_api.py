# python discord_reg_api.py --email="example@gmail.com" --login="example"


import json
import os
import random
import string
import requests
import argparse

from twocaptcha import TwoCaptcha

API_2CAPTCHA = 'example'


def file_save(email, login, password, token):
    with open("data.txt", "w") as file:
        file.write(f'''
		email = {email}
		login = {login}
		password = {password}
		token = {token}
		''')


def password_generation(password_len: int) -> str:
    password = []
    ascii = string.ascii_letters + string.digits
    for _ in range(password_len):
        password.append(random.choice(ascii))
    return password


def captcha_solv() -> str:
    api_key = os.getenv('APIKEY_2CAPTCHA', API_2CAPTCHA)

    solver = TwoCaptcha(api_key)

    try:
        result = solver.hcaptcha(
            sitekey='4c672d35-0701-42b2-88c3-78380b0db560',
            url='https://discord.com/register',
        )

    except Exception as e:
        print(e)
        return False

    else:
        return result


parser = argparse.ArgumentParser(
    description='Discord registration using api v9')
parser.add_argument('--email', type=str)
parser.add_argument('--login', type=str, help='login/name')
args = parser.parse_args()

EMAIL_USER_INPUT = str(args.email)
LOGIN_USER_INPUT = str(args.login)
PASSWORD_GENERATED = password_generation(32)


def api_reg():
    data = {
        "fingerprint": "1010991204462248048.H1BH2iKetTMQvUQLKRT1855Y0mg",
        "email": EMAIL_USER_INPUT,
        "username": LOGIN_USER_INPUT,
        "password": PASSWORD_GENERATED,
        "invite": "null",
        "consent": "true",
        "date_of_birth": "2005-03-04",
        "gift_code_sku_id": "null",
        "captcha_key": str(captcha_solv()['code']),
        "promotional_email_opt_in": "false"
    }

    data = json.loads(json.dumps(data))

    headers = {
        'Content-Type': 'application/json'
    }

    r = requests.post('https://discord.com/api/v9/auth/register',
                      data=data, headers=headers)
    return r


if __name__ == '__main__':
    token = api_reg()['token']
    print(f'Ваший токен: {token}')
    file_save(EMAIL_USER_INPUT, LOGIN_USER_INPUT, PASSWORD_GENERATED, token)
