# -*- coding: utf-8 -*-
from fabric.api import run, task

def print_result(res):
    print "--- print res ---"
    print res
    print "-----------------"
    print "res.return_code:", res.return_code
    print "res.succeeded:", res.succeeded
    print "res.failed:", res.failed
    print "res.command:", res.command
    print "res.real_command:", res.real_command
    print


@task
def test_normal():
    print "=== case 0 ==="
    res = run('/pass_to_command/testcommand.sh 0')
    print_result(res)

    print "=== case 1 ==="
    res = run('/pass_to_command/testcommand.sh 1')
    print_result(res)

@task
def test_warn_only():
    print "=== case 0 ==="
    res = run('/pass_to_command/testcommand.sh 0', warn_only=True)
    print_result(res)

    print "=== case 1 ==="
    res = run('/pass_to_command/testcommand.sh 1', warn_only=True)
    print_result(res)

@task
def test_quiet():
    print "=== case 0 ==="
    res = run('/pass_to_command/testcommand.sh 0', quiet=True)
    print_result(res)

    print "=== case 1 ==="
    res = run('/pass_to_command/testcommand.sh 1', quiet=True)
    print_result(res)

