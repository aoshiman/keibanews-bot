#!/bin/bash
export LANG=ja_JP.utf-8
export ENV_NAME=keibanews-bot
export VIRTUALENV_PATH=$HOME/.virtualenvs/$ENV_NAME
source $VIRTUALENV_PATH/bin/activate
cd $HOME/dev/keibanews-bot
python ./keibanews_bot.py tweet
exit
