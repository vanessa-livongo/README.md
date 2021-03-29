#!/usr/bin/env python3
import os
import logging
import requests
import json
import datetime

def create_branch(owner: str, repo: str, base: str, new_branch: str) -> None:
    url = "https://api.github.com/repos/{}/{}/git/refs".format(owner, repo)
    headers = {
        "Authorization": "token {}".format(GITHUB_TOKEN),
        "Content-Type": "application/json"
    }
    try:
        get_response = requests.get(url+"/heads/"+base, headers=headers)
        sha = json.loads(get_response.content)['object']['sha']
        payload = {
            "ref": "refs/heads/"+new_branch,
            "sha": sha
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            logging.error(json.loads(response.content))
    except requests.exceptions.RequestException as e:
        logging.error(e)

def create_pull_request(owner: str, repo: str, new_branch: str, base: str) -> None:
    url = "https://api.github.com/repos/{}/{}/pulls".format(owner, repo)
    headers = {
        "Authorization": "token {}".format(GITHUB_TOKEN),
        "Content-Type": "application/json"
    }
    payload = {
        "head": new_branch,
        "base": base
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            logging.error(json.loads(response.content)['errors'][0]['message'])
    except requests.exceptions.RequestException as e:
        logging.error(e)

def get_file_sha(owner: str, repo: str, filename: str) -> str:
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(owner, repo, filename)
    headers = {
        "Authorization": "token {}".format(GITHUB_TOKEN),
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code != 200:
            logging.error(json.loads(response.content)['errors'][0]['message'])
    except requests.exceptions.RequestException as e:
        logging.error(e)
# def update_file_contents(owner: str, repo: str):
#     url = "https://api.github.com/repos/{}/{}/contents/locations.data-ops.daily.json".format(owner, repo)
#     payload = {
#         "message": new_branch,
#         "base": base
#     }
#     try:
#         response = requests.put(url, headers=headers, json=payload)
#         if response.status_code != 200:
#             logging.error(json.loads(response.content)['errors'][0]['message'])
#     except requests.exceptions.RequestException as e:
#         logging.error(e)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    try:
        GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    except KeyError as e:
        logging.error(e)
    
    GITHUB_OWNER = "vanessa-livongo"
    GITHUB_REPO = "vanessa-livongo"
    get_file_sha(GITHUB_OWNER, GITHUB_REPO, "locations.data-ops.daily.json")
    # import fileinput

    # with fileinput.FileInput("locations.data-ops.daily.json", inplace=True, backup='.bak') as file:
    #     for line in file:
    #         print(line.replace("data/TEST", "data/TEST_FOLDER"), end='')
    # create_branch("vanessa-livongo", "vanessa-livongo", "main", datetime.date.today().strftime('%Y-%m-%d'))
    # create_pull_request("vanessa-livongo", "vanessa-livongo", "main", datetime.date.today().strftime('%Y-%m-%d'))