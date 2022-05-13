# Validate Issues over Pull Requests

[![Action Template](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/HarshCasper/validate-issues-over-pull-requests)
[![Lint](https://github.com/HarshCasper/validate-issues-over-pull-requests/actions/workflows/ci.yml/badge.svg)](https://github.com/HarshCasper/validate-issues-over-pull-requests/actions/workflows/ci.yml)

A GitHub Action to validate submitted Pull Requests to check if they have a valid Issue present in the body. The contributors are usually expected to link Issues to Pull Requests using key phrases like `Fixes #XYZ` or `Resolves #XYZ`. This Action validates if an Issue is present over the Pull Request body and lets the maintainer take further prompt over specific Pull Requests!

## Usage

To get started, you can use this minimal example:

```yml
name: Check if a PR has a valid Issue

on:
  pull_request_target:
    types: [ edited, synchronize, opened, reopened ]

jobs:
  checker:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      
      - name: Issue Validator
        uses: HarshCasper/validate-issues-over-pull-requests@v0.1.1
        id: validator
        with:
          prbody: ${{ github.event.pull_request.body }}
          prurl: ${{ github.event.pull_request.url }}
```

### Inputs

|Input|Description  |Example
|--|--|--|
|prbody  |The Pull Request body to be analyzed  | `${{ github.event.pull_request.body }}`
|prurl  |The Pull Request URL to be analyzed  | `${{ github.event.pull_request.body }}`

### Output

|Output|Description  |
|--|--|
|valid  |Boolean that denotes if a Pull Request body has a valid Issue (`1` if its present and `0` if its not)  |

### Example Workflow

As a maintainer, if you wish to take an opinionated way of tagging/labeling Pull Requests which contain (or may not contain) a valid Issue, here is an example:

```yml
name: PR has a valid Issue?

on:
  pull_request_target:
    types: [ edited, synchronize, opened, reopened ]

jobs:
  checker:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      
      - name: Issue Validator
        uses: HarshCasper/validate-issues-over-pull-requests@v0.1.1
        id: validator
        with:
          prbody: ${{ github.event.pull_request.body }}
          prurl: ${{ github.event.pull_request.url }}
          
      - name: PR has a valid Issue
        if: ${{ steps.validator.outputs.valid == 1 }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PRNUM: ${{ github.event.pull_request.number }}
        run: |
          gh pr edit $PRNUM --add-label "PR:Ready-to-Review"
          gh pr edit $PRNUM --remove-label "PR:No-Issue"
          
      - name: PR has no valid Issue
        if: ${{ steps.validator.outputs.valid == 0 }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PRNUM: ${{ github.event.pull_request.number }}
        run: |
          gh pr comment $PRNUM --body "PR is not linked to any issue, please make the corresponding changes in the body."
          gh pr edit $PRNUM --add-label "PR:No-Issue"
 ```
 
However you can mould the above logic and use the [GitHub's CLI](https://cli.github.com/) `gh` to develop your own preferred workflow.

## Acknowledgments

The Action is based on the awesome work done by  [XZANATOL](https://github.com/XZANATOL) for [Rotten Scripts](https://github.com/HarshCasper/Rotten-Scripts). We have been using this Action for some time now to mark Pull Requests that are not linked to any Issue. Based on a [Stack Overflow question](https://stackoverflow.com/questions/72009749/how-to-trigger-github-workflows-on-link-issue-to-pr), I decided to publish this Action for a more general use case and further maintain it.

## License

[MIT License](https://github.com/HarshCasper/validate-issues-over-pull-requests/blob/main/LICENSE)
