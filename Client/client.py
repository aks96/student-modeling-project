import requests
import json
import cutie
from functools import reduce

token = None
responses = []


def create_account():
    global token

    name = input('Enter your name: ')
    username = input('Enter a username: ')
    pwd = cutie.secure_input('Select a password: ')

    r = requests.post('http://localhost:5000/api/user/signup', json={
        'name': name,
        'username': username,
        'password': pwd
    })

    # Check 409 Conflict
    if r.status_code == 409:
        print('Username already exists.')
        return

    token = r.json()['token']
    print('Account successfully created. You are now logged in.')


def login():
    global token

    username = input('Enter your username: ')
    pwd = cutie.secure_input('Enter your password: ')

    r = requests.post('http://localhost:5000/api/user/login', json={
        'username': username,
        'password': pwd
    })

    # Check 401 Unauthorized
    if r.status_code == 401:
        print('Incorrect username or password.')
        return

    token = r.json()['token']
    print('Login successful.')


def next_question():
    global token

    if token is not None:
        print('You must first log in.')
        return

    r = requests.post('http://localhost:5000/api/session/get_question', json={
        'token': token
    })

    if r.status_code == 401:
        print('Please log in again.')
        return

    data = r.json()
    question = data['question']
    answer = data['answer']
    options = data['options']

    # We need to do two things: check the answer and inform the user of
    # the result, and store this info
    selected = cutie.select(options, selected_index=0)
    if selected == answer:
        print('Correct!')
    else:
        print('Incorrect: The right answer is', answer)

    if r.status_code != 200:
        print(r.json())

    responses.append({
        'question_id': data['question_id'],
        'response': selected,
        'correct': answer
    })

    print('\n\n')


def start_session():
    global token, responses

    questions = 0

    # Continue showing more questions as long as user wants
    while True:
        next_question()
        questions += 1

        if not cutie.prompt_yes_or_no('Continue?'):
            break

    # Show basic statistics
    print('Questions answered:', questions)
    print('Correctly answered:', reduce(
        lambda obj: obj['response'] == obj['correct'],
        responses))

    # Pass data to server
    r = requests.post('http://localhost:5000/api/session/end', json={
        'token': token,
        'responses': responses
    })


def stop():
    exit(0)


if __name__ == '__main__':
    while True:
        options = [
            'Login',
            'Sign up',
            'Start session',
            'Quit'
        ]

        option = cutie.select(options, selected_index=0)
        actions = [login, create_account, start_session, stop]

        actions[option]()
