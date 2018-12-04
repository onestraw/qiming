# coding=utf-8
import sys
import subprocess


def _compat(text):
    if sys.version_info[0] == 2:
        return text
    if isinstance(text, bytes):
        return text.decode('utf-8')
    return text.encode('utf-8')


def convert(text, config):
    proc = subprocess.Popen(['opencc', '-c', config],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    result, err = proc.communicate(_compat(text))
    if proc.returncode:
        raise RuntimeError('Failed to call opencc with exit code {}'.
                           format(proc.returncode))
    return _compat(result)


def s2t(text):
    return convert(text, 's2t')


def t2s(text):
    return convert(text, 't2s')


if __name__ == '__main__':
    print(s2t('华'))
    print(t2s('華'))
