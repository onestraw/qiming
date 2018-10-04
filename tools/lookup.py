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
    body = open(json_file).read()

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

    with open(index_file, 'w+') as f:
        f.write(json.dumps(index))


def lookup(word):
    if not os.path.exists(WordIndexJson):
        create_index(RawWordJson, WordIndexJson)

    index = json.loads(open(WordIndexJson).read())
    if word not in index:
        return ''

    offset, limit = index[word]
    with open(RawWordJson) as f:
        f.seek(offset)
        record = f.read(limit)
    try:
        data = json.loads(record)
        return data['explanation']
    except Exception as e:
        print(e.message)
        return record


if __name__ == '__main__':
    w = u'天'
    print(lookup(w))
