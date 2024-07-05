#!/bin/bash

function _clear ()
{
  read -n1
  clear
}

function _prompt ()
{
  echo -ne "\033[01;32mp4bl0@romuald\033[00m:\033[01;34m~/research/code/thc/scripts\033[00m\$ "
  echo -en "\033]0;p4bl0@romuald: ~/research/code/thc/scripts\a"
}

function _cmd ()
{
  echo -ne "$*"
  read -n1
  echo -ne "\033]0;p4bl0@romuald: ~/research/code/thc/scripts\$ $1\a"
  $*
}

clear
_prompt
_cmd pygmentize -O style=rrt cans2021-trivial.py
_prompt
_cmd python3 cans2021-trivial.py
_prompt
_cmd python3 cans2021-trivial.py
_prompt

_clear
_prompt
_cmd pygmentize -O style=rrt cans2021-examples.py
_prompt
_cmd python3 cans2021-examples.py
_prompt

_clear
_prompt
_cmd pygmentize -O style=rrt cans2021-examples_small-r.py
_prompt
_cmd python3 cans2021-examples_small-r.py
_prompt
read -n1 RE
while [ "$RE" = "!" ]; do
  echo -ne "\r"
  _prompt
  _cmd python3 cans2021-examples_small-r.py
  _prompt
  read -n1 RE
done

clear
_prompt
_cmd pygmentize -O style=rrt cans2021-examples_known-r.py
_prompt
_cmd python3 cans2021-examples_known-r.py
_prompt

_clear
_prompt
_cmd pygmentize -O style=rrt cans2021-examples_known-r_2.py
_prompt
_cmd python3 cans2021-examples_known-r_2.py
_prompt

_clear
_prompt
_cmd pygmentize -O style=rrt cans2021-examples_known-r_3.py
_prompt
_cmd python3 cans2021-examples_known-r_3.py
_prompt

_clear
_prompt
_cmd python3 cans2021-usecase.py
_prompt
_cmd python3 cans2021-usecase.py
_prompt
_cmd python3 cans2021-usecase.py
