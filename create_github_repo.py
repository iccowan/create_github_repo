# Create a GitHub Repo from the command line

# Import Packages
import requests


def get_github_token():
    # Open the config file, get the token, and return it
    config_file = open('config.config', 'r')
    token = ''
    for line in config_file:
        line_list = line.strip().split('=')
        if line_list[0] == 'github_api_key':
            try:
                token = line_list[1]
            except IndexError:
                pass

    if token == '':
        raise Exception('NoToken: No GitHub token found in config.config')

    return token


def create_repo(name, desc, homepage, is_private):
    # Get the token
    token = get_github_token()

    # Add the data to a dictionary
    data = {
        'name': name,
        'description': desc,
        'homepage': homepage,
        'private': is_private
    }

    # Add the headers to a dictionary
    headers = {
        'Authorization': 'token ' + token
    }

    # Make the call
    response = requests.post('https://api.github.com/user/repos', json=data, headers=headers).json()
    ssh_url = response['ssh_url']
    http_url = response['html_url']

    return ssh_url, http_url


def main():
    # Get all of the required information from the user
    name = input('Name of the repository: ').strip()
    while name == '':
        print('The name field is required.')
        name = input('Name of the repository: ').strip()
    desc = input('Description: ').strip()
    homepage = input('Homepage: ').strip()
    private = input('Private? [y/n]: ').strip().upper()

    # Convert private to a boolean
    if private == 'Y':
        is_private = True
    else:
        is_private = False

    # Make the request
    ssh_url, http_url = create_repo(name, desc, homepage, is_private)

    # Let the user know everything was successful and what the URL is
    print()
    print('Repository created successfully!')
    print('SSH URL: ' + ssh_url)
    print('HTTP URL: ' + http_url)


main()
