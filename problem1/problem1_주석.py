import string
import os
import re
from tkinter import *
import numpy as np
import pandas as pd


class problem1:
    ### class명은 CamelCase를 사용함: 각 단어의 처음이 대문자로 problem1 -> Problem1

    def __init__(self):
        ### init 함수에서는 class 내부에서 사용할 변수명이 있으면 선언 해 줄 것: ex) self._var
        ### 초기 셋팅 값이 있으면 파라미터를 입력 받을 것
        # 문자열에서 영문, 숫자를 제외한 문자열 제거하기
        pass

    # remove punctuation :https://towardsdatascience.com/nlp-for-beginners-cleaning-preprocessing-text-data-ae8e306bef0f
    def remove_punctuation(self, text):
        '''
        function에는 이와 같은 형식으로 함수의 구조와 파라미터의 대한 설명 리턴내용들을 미리 기술 하면 좋음
        함수 위에 기능에 대한 설명 달아 놓은 것을 여기로 옮길 것
        pucntuation은 구두점을 얘기하는데 특수문자와는 다름 의미이므로 네이밍을 다시 고려해 보는것이 좋을 듯
        :param text:
        :return:
        '''
        no_punct = "".join([c for c in text if c not in string.punctuation])
        return no_punct

    # get input punctuation and remove them
    def input_remove_punctuation(self, text, punc):
        punc += '\n'
        ### list comprehension외에 다른 방식으로 처리할 수 있는지 고민할 것
        no_punct = "".join([c for c in text if c not in punc])
        return no_punct

    # substitute punctuation to '\n'
    def replace_punctuation(self, text):
        """
        punc = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        no_punct = re.sub("[^A-Za-z0-9-' '-'\'-\'-']+", ' ', text)
        punc = string.punctuation + "'" + '-' + ','
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punct = " ".join(word.strip(punc) for word in text.split())
        print(no_punct)
        no_punct = re.sub(punc, ' ', text)
        no_punct = text.translate({ord(x): y for (x, y) in zip(punc, len(punc)*' ')})
        """
        no_punct = re.sub(r'[^\w\s]',' ', text)
        no_punct = re.sub(r'\_', '', no_punct)
        no_punct = re.sub(r'\n', '', no_punct)

        return no_punct

    # input extension option
    def getResultOption(self):
        fileName = input("[file name with extension]\n"
                         "(extension: csv, txt, json)\n")
        fName = fileName.split('.')[0]
        extension = fileName.split('.')[1]
        print(fName, extension)

        return fName, extension

    # save result by extension option
    def getResult(self, data):
        ### 기능과 함수명을 일치시키도록 노력! -> getResult 이지만 실제로 파일에 결과룰 출력하는 것이기 때문에 write에 가까움
        
        fn, ext = self.getResultOption()
        if (ext == "csv"):
            # result to csv
            data.to_csv(fn + '.csv', index=False, header=['docNum', 'text'])
        elif (ext == "txt"):
            # result to txt
            fn = fn + '.txt'
            with open(fn, 'w') as f:
                f.write(data.to_string(header=False, index=False))
        elif (ext == "json"):
            # result to json
            fn = fn + '.json'
            data.to_json(fn, orient='table')
        else:
            print("Error: Write Another Extension (csv, txt, json)")
            self.getResult(data)

    def main(self):
        ### main안에 기능을 전부 넣는 것이 아닌 기능 단위로 분리할 것 ex) main과 같은 함수에서는 주로 함수 호출부만 만들 것
        fname, ext = os.path.splitext('input.txt')
        #print(fname)
        #print(ext)
        fileName = fname + ext
        fileName = input("- Input file name with extension: ")

        # read txt file
        try:
            with open(fileName, 'r') as file:
                a = file.readlines()
        except FileNotFoundError as e:
            ### 예외 내용 e만 출력하는 것이 아닌 예외 내용을 직접 기술하면 더 좋음 ex) print('예외 내용: {}'.format(e))
            print(e)

        # get document number & remove doc number in text
        fNum = []
        index = 0
        for line in a:
            if line.split(' ')[0].isdigit() == True:
                fNum.append(int(line.split(' ')[0]))
                a[index] = line.replace(line.split(' ')[0], '')
                index += 1

        data = {'docNum': fNum, 'text': a}
        data = pd.DataFrame(data)
        #print(data)
        #print(string.punctuation)

        ### 솔루션에서는 키보드 입력보다는 property 파일을 만들어서 실행 시키는 것이 좋음
        ### 키보드 입력받으면 중간중간 사용자가 입력을 해 줘야 하기 때문에 interupt가 걸림
        punc = int(input("1 - punctuation directly setting (Remove punctuation)\n"
                     "2 - existed punctuation usage (Replace to spacebard)\n"))

        if(punc == 1):
            punc = input("[Punctuation]\n"
                        "(just write each punctuation without spacebar and write Enter key when you are done)\n")
            data['text'] = data['text'].apply(lambda x: self.input_remove_punctuation(x, punc))
        elif(punc == 2):
            data['text'] = data['text'].apply(lambda x: self.replace_punctuation(x))

        #data['text'] = data['text'].apply(lambda x: self.remove_punctuation(x))
        # print(data.iloc[3])
        print(data)

        self.getResult(data)


###  main을 별로도 명시하여 시작점을 따로주는 것이 좋음
if __name__ == "__main__":

    ### 클래스 선언 변수명은 소문자로 P -> p
    P = problem1()
    
    ### main 부터 시작이 아닌 run()또는 기능 함수의 이름으로 시작할 것
    P.main()