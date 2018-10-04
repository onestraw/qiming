# coding=utf-8

import os
import json


RawWordJson = 'data/word.json'
WordIndexJson = 'data/word_index.json'


class State(object):
    # state machine
    BlockEnd = 1
    BlockBegin = 2
    BeforeWordBegin = 3
    Word = 4
    WordEnd = 5


def create_index(json_file, index_file):
    f = open(json_file)
    body = f.read()
    f.close()

    # key: [offset, limit]
    index = {}
    word = []
    offset = -1
    limit = -1

    state = State.BlockEnd
    for i, c in enumerate(body):
        if state == State.BlockEnd:
            if c == '{':
                offset = i
                state = State.BlockBegin
        elif state == State.BlockBegin:
            if c == ':':
                state = State.BeforeWordBegin
        elif state == State.BeforeWordBegin:
            if c == '"':
                state = State.Word
        elif state == State.Word:
            if c == '"':
                state = State.WordEnd
            else:
                word.append(c)
        elif state == State.WordEnd:
            if c == '}':
                limit = i - offset + 1
                index[''.join(word)] = [offset, limit]
                word = []
                state = State.BlockEnd

    f = open(index_file, 'w+')
    f.write(json.dumps(index))
    f.close()


def lookup(word):
    if not os.path.exists(WordIndexJson):
        create_index(RawWordJson, WordIndexJson)
    f = open(WordIndexJson)
    index = json.loads(f.read())
    f.close()

    if word not in index:
        return ''

    offset, limit = index[word]
    f = open(RawWordJson)
    f.seek(offset)
    record = f.read(limit)
    f.close()
    try:
        data = json.loads(record)
        return data['explanation']
    except Exception as e:
        print(e.message)
        return record


if __name__ == '__main__':
    w = u'天'
    print(lookup(w))
