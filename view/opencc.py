# coding=utf-8
import subprocess


def convert(text, config):
    proc = subprocess.Popen(['opencc', '-c', config],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    result, err = proc.communicate(text)
    if proc.returncode:
        raise RuntimeError('Failed to call opencc with exit code {}'.
                           format(proc.returncode))
    return result


def s2t(text):
    return convert(text, 's2t')


def t2s(text):
    return convert(text, 't2s')


if __name__ == '__main__':
    print(s2t('华'))
    print(t2s('華'))
