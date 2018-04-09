import re
import sys
import hashlib
import json
import random
import requests
import argparse
import urllib.parse
import trans.config

LANGUAGE_DICT = {
    '-j': 'ja',
    '-e': 'EN',
    '-k': 'ko',
    '-f': 'fr',
    '-r': 'ru',
    '-p': 'pt',
    '-es': 'es',
    '--japanese': 'ja',
    '--english': 'EN',
    '--korean': 'ko',
    '--france': 'fr',
    '--russian': 'ru',
    '--portuguesa': 'pt',
    '--espana': 'es',
}


class Translate:

    def __init__(self, args):
        if len(args) == 0:
            print("ERROR: PLEASE INPUT WORD \n")
            return

        self.key = trans.config.main().get("key")
        self.secret = trans.config.main().get("secret")
        word = args[0]
        option = '-e'
        if len(args) > 1:
            if LANGUAGE_DICT.get(args[1]) is None:
                print("ERROR: INVALIDA OPTIONS")
                return
            else:
                option = LANGUAGE_DICT.get(args[1])

        self.translate(word, option)

    def translate(self, word, option):
        toLang = option
        if re.compile(u'[\u4e00-\u9fa5]+').search(word) is False:
            toLang = 'zh-CHS'
        salt = random.randint(1, 65536)
        sign = self.key + word + str(salt) + self.secret
        sign = sign.encode("utf8")
        md5 = hashlib.md5()
        md5.update(sign)
        sign = md5.hexdigest()
        url = 'https://openapi.youdao.com/api' + '?appKey=' + self.key + '&q=' + urllib.parse.quote(word)+'&to='+ toLang + '&salt=' +str(salt)+'&sign='+sign
        try:
            response = requests.get(url)
            res_json = json.loads(response.text)
            print('\n')
            print('\033[1;3m' + word + '\033[0m  \n')
            print("翻译：" + ','.join(res_json['translation']) + '\n')
            if res_json.get('basic'):
                if res_json.get('basic').get('us-phonetic'):
                    print("美音：[" + res_json.get('basic').get('us-phonetic') + ']   英音：[' + res_json.get('basic')['uk-phonetic'] + '] \n')

                if res_json.get('basic').get('explains'):
                    print("基础释义：" + ','.join(res_json['basic']['explains']) + '\n')

            if res_json.get('web'):
                print("相关释义 \n")
                for i in res_json['web']:
                    print(i['key'] + ':   ' + ','.join(i['value']) + '\n')

        except Exception as e:
            print(e)


if len(sys.argv) == 0:
    sys.argv.append('--help')

parser = argparse.ArgumentParser()
parser.add_argument('-j', '--japanese', help="trans to Japanse")
parser.add_argument('-e', '--english', help="trans to English")
parser.add_argument('-k', '--korean', help="trans to Korean")
parser.add_argument('-f', '--franch', help="trans to Franch")
parser.add_argument('-r', '--russian', help="trans to Russian")
parser.add_argument('-p', '--portuguesa', help="trans to Portuguesa")
parser.add_argument('-es', '--espana', help="trans to Espana")


def main():
    Translate(sys.argv[1:])


if __name__ == '__main__':
    main()

