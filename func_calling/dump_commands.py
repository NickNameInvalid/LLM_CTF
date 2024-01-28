#!/usr/bin/env python3

import json
import sys
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import TerminalFormatter
from ctflogging import status

def print_create_file(args, result):
    filename = result['path']
    content = args['contents']
    lexer = get_lexer_for_filename(filename)
    formatter = TerminalFormatter()
    print(f"Create file {filename}:")
    print(highlight(content, lexer, formatter))

def print_run_command(args, result):
    ret = result['returncode']
    timed_out = " (timed out)" if result['timed_out'] else ""
    print(f"Command exec with ret={ret}{timed_out}:")
    command = args['command']
    stdout = result['stdout']
    stderr = result['stderr']
    print(f"$ {command}")
    if stdout:
        print(f"==> stdout:\n{stdout}")
    if stderr:
        print(f"==> stderr:\n{stderr}")

def print_command(name, args, result):
    if args is None:
        argstr = '[missing]'
    else:
        argstr = ', '.join(f'{k}={repr(v)}' for k, v in args.items())
    if name == "run_command":
        print_run_command(args, result)
    elif name == "createfile":
        print_create_file(args, result)
    else:
        print(f"{name}({argstr}):")
        for k,v in result.items():
            print(f"==> {k}:\n{v}")

calls = {}
js = json.load(open(sys.argv[1]))
print(f"Log of conversation {js['start_time']} to {js['end_time']} ({js['runtime_seconds']} seconds)")
solve_str = "solved successfully" if js['solved'] else "not solved"
print(f"Conversation lasted {js['rounds']} rounds and was {solve_str}")
print("*"*80)
for message in js['messages']:
    if message['content']:
        if message['role'] == 'system':
            status.system_message(message['content'])
        elif message['role'] == 'user':
            status.user_message(message['content'])
        elif message['role'] == 'assistant':
            status.assistant_message(message['content'])

    if 'tool_calls' in message and message['tool_calls']:
        for tool_call in message['tool_calls']:
            call_id = tool_call['id']
            function = tool_call['function']
            name = function['name']
            args = json.loads(function['arguments'])
            calls[call_id] = (name, args)
    elif message['role'] == 'tool':
        call_id = message['tool_call_id']
        name = message['name']
        if call_id in calls:
            args = calls[call_id][1]
        else:
            args = None
        result = json.loads(message['content'])
        print_command(name, args, result)
    print("="*80)
