__author__ = 'sanyi'

import fcntl
import os
import time
import subprocess
from .exceptions import *

IPSET_COMMAND = 'ipset'
IPSET_TIMEOUT = 2


def _process_error_message(msg):
    if "Kernel error received: Operation not permitted" in msg:
        raise IpsetNoRights(msg)
    elif "The set with the given name does not exist" in msg:
        raise IpsetSetNotFound(msg)
    elif "is NOT in set" in msg:
        raise IpsetEntryNotFound(msg)
    raise IpsetError(msg)


def ipset_send_command(*arguments, **kv_arguments):

    try:

        command_timeout = kv_arguments.get('command_timeout', IPSET_TIMEOUT)
        if command_timeout is None:
            command_timeout = IPSET_TIMEOUT

        command_list = kv_arguments.get('command_list', None)

        process = subprocess.Popen((IPSET_COMMAND, ) + arguments, universal_newlines=True,
                                   stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        if command_list:
            for command in command_list:
                process.stdin.write(command)

        result, error = process.communicate(timeout=command_timeout)

    except subprocess.TimeoutExpired:
        process.kill()
        raise IpsetCommandHangs()
    except FileNotFoundError:
        raise IpsetNotFound()

    if process.returncode != 0:
        _process_error_message(error)

    return result


def ipset_send_command_g(*arguments, **kv_arguments):

    try:

        command_timeout = kv_arguments.get('command_timeout', IPSET_TIMEOUT)
        if command_timeout is None:
            command_timeout = IPSET_TIMEOUT

        command_list = kv_arguments.get('command_list', None)

        process = subprocess.Popen((IPSET_COMMAND, ) + arguments, universal_newlines=True,
                                   stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        if command_list:
            for command in command_list:
                process.stdin.write(command)

        stdout_fileno = process.stdout.fileno()
        fcntl.fcntl(stdout_fileno, fcntl.F_SETFL, fcntl.fcntl(stdout_fileno, fcntl.F_GETFL) | os.O_NONBLOCK)

        data = ""

        expire_time = time.time() + command_timeout

        while True:
            try:
                data_part = process.stdout.read()
                if not data_part:
                    yield data
                    break

                data += data_part

                while True:
                    p = data.find("\n")
                    if p == -1:
                        break
                    yield data[:p]
                    expire_time = time.time() + command_timeout
                    data = data[p+1:]
            except:
                # python3.4 raises rather improper exception "TypeError: can't concat bytes to NoneType" on failed read

                if time.time() > expire_time:
                    if process.poll() is None:
                        process.kill()
                    raise IpsetCommandHangs()

                time.sleep(0.1)

    except FileNotFoundError:
        raise IpsetNotFound()

    if process.poll() is None:
        process.wait(command_timeout)

    if process.returncode != 0:
        stderr_fileno = process.stderr.fileno()
        fcntl.fcntl(stderr_fileno, fcntl.F_SETFL, fcntl.fcntl(stderr_fileno, fcntl.F_GETFL) | os.O_NONBLOCK)
        try:
            error = process.stderr.read()
        except:
            error = '-'
        _process_error_message(error)


def ipset_create_set(set_name, type_name, exist=False, command_timeout=None):
    arguments = ["create", set_name, type_name]
    if exist:
        arguments.append('-exist')
    return ipset_send_command(*arguments, command_timeout=command_timeout)


def ipset_add_entry(set_name, entry, entry_timeout=None, exist=False, command_timeout=None):
    arguments = ["add", set_name, entry]
    if entry_timeout:
        arguments.append("timeout")
        arguments.append("%d" % (int(entry_timeout),))
    if exist:
        arguments.append('-exist')
    return ipset_send_command(*arguments, command_timeout=command_timeout)


def ipset_del_entry(set_name, entry, exist=False, command_timeout=None):
    arguments = ["del", set_name, entry]
    if exist:
        arguments.append('-exist')
    return ipset_send_command(*arguments, command_timeout=command_timeout)


def ipset_test_entry(set_name, entry, command_timeout=None):
    try:
        ipset_send_command("test", set_name, entry, command_timeout=command_timeout)
        return True
    except IpsetEntryNotFound:
        return False


def ipset_destroy_set(set_name, command_timeout=None):
    return ipset_send_command("destroy", set_name, command_timeout=command_timeout)


def ipset_list(set_name=None, resolve=False, sort=False, name=False, terse=False, file_path=False,
               output='plain', generator=False, command_timeout=None):

    arguments = ["list"]
    if set_name:
        arguments.append(set_name)
    if terse:
        arguments.append("-terse")
    if resolve:
        arguments.append("-resolve")
    if sort:
        arguments.append("-sorted")
    if name:
        arguments.append("-name")
    if file_path:
        arguments.append("-file")
        arguments.append(file_path)
    if output:
        arguments.append("-output")
        arguments.append(output)

    if not generator:
        return ipset_send_command(*arguments, command_timeout=command_timeout)
    else:
        return ipset_send_command_g(*arguments, command_timeout=command_timeout)


def ipset_save(set_name=None, file_path=None, command_timeout=None):

    arguments = ["save"]
    if set_name:
        arguments.append(set_name)
    if file_path:
        arguments.append('-file')
        arguments.append(file_path)

    return ipset_send_command(*arguments, command_timeout=command_timeout)


def ipset_restore_from_file(file_path, command_timeout=None):
    return ipset_send_command("restore", '-file', file_path, command_timeout=command_timeout)


def ipset_restore_from_command_list(command_list, command_timeout=None):
    return ipset_send_command("restore", command_list=command_list, command_timeout=command_timeout)


def ipset_flush_set(set_name, command_timeout=None):
    return ipset_send_command("flush", set_name, command_timeout=command_timeout)


def ipset_rename(set_name_from, set_name_to, command_timeout=None):
    return ipset_send_command("rename", set_name_from, set_name_to, command_timeout=command_timeout)


def ipset_swap(set_name_from, set_name_to, command_timeout=None):
    return ipset_send_command("swap", set_name_from, set_name_to, command_timeout=command_timeout)


def ipset_version(command_timeout=None):
    return ipset_send_command("version", command_timeout=command_timeout)
