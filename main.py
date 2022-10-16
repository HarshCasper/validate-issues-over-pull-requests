import os
import re

import requests


def main():
    """
    Function to validate the Issue present over the Pull Request body.
    """

    pattern = "((?:Fixes|Resolves) #\d+)"

    # Get the PR body and the PR URL
    body = os.getenv("INPUT_PRBODY")
    url = os.getenv("INPUT_PRURL")
    print(body)
    print(url)

    # Get the Issue number
    try:
        issue_num = re.search(pattern, body)[0].replace("#", "")
        print(issue_num)
    except:
        issue_num = "No issue number"

    # URL List will match: ['https:', '', 'api.github.com', 'repos', 'owner', 'repo-name']
    url = url.split("/")[:-2]
    url[2] = url[2].replace("api.", "")

    # Get rid of the repos record
    url.pop(3)

    # Reattach the URL pieces
    url = "/".join(url)

    # Add the issue number to the URL
    url += "/issues/{}".format(issue_num)
    print(url)

    # Check if its valid code
    valid_code = 0
    response = requests.get(url)
    if response.status_code == 200:
        if response.url == url:
            # Check if issue is open or closed
            text = response.text
            pattern_issue = "Status:\s(\w+)"
            if re.search(pattern_issue, text)[1] == "Open":
                valid_code = 1
            else:
                print("Issue is closed")
    else:
        print(
            "Invalid Response Code obtained - error code: {}".format(
                response.status_code
            )
        )

    print("Valid flag is:", valid_code)
    print(f"::set-output name=valid::{valid_code}")


if __name__ == "__main__":
    main()
