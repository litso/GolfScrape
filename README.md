# Intro
Periodically checks the booking site for availability for a local golf course at a desireable tee time.
If one is found, sends a text message via [AWS pinpoint](https://aws.amazon.com/blogs/compute/building-a-serverless-weather-bot-with-two-way-sms-aws-sam-and-aws-lambda/) to a phone number.

Setup and deployment to AWS is done via Serverless.

# Setup

## Setup Python


### Install Pyenv

```
brew update && brew upgrade pyenv
# Will install correct version of python specified in .python-version
pyenv install
```

### Create the Virtual Environment

Create the environment
```
python3 -m venv env
```

And Activate It

```
# Bash or ZSH
source env/bin/activate

# or Fish
. env/bin/activate.fish
```

## Install Serverless


### Install Node

Check you node version. As of this writing i'm using 7.3.

```
npm install -g serverless
```

Check the Serverless Version

```
serverless --version
2.16.1
```

Install Python Requirements Plugin

```
npm install
sls plugin install -n serverless-python-requirements
```

Note if you see an error about an unsupported engine, its because our package.json locks the NPM version to 7.3. Either install that version of NPM or use something like NVM to install the correct version.

## Headless Chrome
In order to use headless chrome on AWS Lambda, we need to configure a layer to include both of the binaries. This will defer on your local system since the binaries will be different.

## Chrome Layer
Unzip headless-chromium.zip or download newer versions:

Download [Headless Chrome](https://github.com/adieuadieu/serverless-chrome/releases/tag/v1.0.0-57)
Download [Chrome Driver](https://chromedriver.storage.googleapis.com/index.html?path=86.0.4240.22/)

## Mimic Chrome Layer for Local Invoke on OSX

Download the Chrome driver that matches the version of Chrome on your local system. Move it to `/opt/chromedriver`

Sym link your local chrome to the right location.

```
cd /opt
ln -s headless-chromium "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
```

# Run Tests Locally

```
env PYTHONPATH=. pytest
```

