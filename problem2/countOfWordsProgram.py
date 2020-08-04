import sys
import yaml
import pandas as pd

class CountOfWordsProgram:

    def __init__(self):
        pass

    def get_property(self):
        '''
        get property file and get input file name, specific words to get the number of them and output file name
        :return: data with object type
        '''
        with open("property.yml") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        return data

    def read_data_from_file(self, propertyData):
        '''
        get option from property file
        :param propertyData: data from property
        :return: data from input file
        '''

        inputFileName = propertyData['input']
        try:
            with open(inputFileName, 'r') as file:
                inputData = file.readlines()
        except FileNotFoundError as e:
            print('해당하는 파일이 없습니다: {}'.format(e))

        return inputData

    def split_data_by_blank(self, text):
        '''
        split the text by blanks
        :param text: text data from input file
        :return: text data splitted by blank
        '''

        blankData = []
        for line in text:
            blankData.append(line.split())

        return blankData

    def find_count_words(self, words, blankData):
        '''
        fine the specific words and count the words in text data
        :param words: words that have to be counted
        :param blankData: text splited by blank
        :return: count
        '''
        wordsList = words.split(',')

        totalCount = 0
        count = [0 for i in range(len(wordsList))]
        for sentence in blankData:
            for wordInSentence in sentence:
                totalCount += 1
                for wIndex in range(len(wordsList)):
                    if(wordInSentence == wordsList[wIndex]):
                        count[wIndex] += 1

        print('the number of words in text data:', totalCount)

        for c in count:
            if c == 0:
                print("------------------------------------------------------------------")
                print("@Warning! count value is 0.")
                print("Check the property file: 'word' have to be splitted by just ','.")
                print("------------------------------------------------------------------")

        return count

    def write_result_data(self, propertyData, count):
        '''
        output file name and extension option to save results by extension option
        :param propertyData: data from property
        :param count: count that have to be saved in output file
        :return: nothing
        '''

        outputFileName = propertyData['output']
        fileName = outputFileName.split('.')[0]
        try:
            ext = outputFileName.split('.')[1]
        except IndexError as e:
            print("'property' 파일의 'output'에 파일 확장자를 붙여서 적어주시기 바랍니다: {}".format(e))


        words = propertyData['word']
        wordsList = words.split(',')

        data = pd.DataFrame({'word':wordsList, 'count':count})

        if (ext == "csv"):  # result to csv
            try:
                data.to_csv(fileName + '.csv', index=False, header=['word', 'count'])
            except PermissionError as e:
                print("해당 CSV파일을 닫아주시기 바랍니다: {}".format(e))
        elif (ext == "txt"):  # result to txt
            fileName = fileName + '.txt'
            with open(fileName, 'w') as file:
                for c in range(len(count)):
                    file.writelines(str(wordsList[c]) + " " + str(count[c]) + "\n")
        elif (ext == "json"):  # result to json
            fileName = fileName + '.json'
            data.to_json(fileName, orient='table')
        else:
            print("Error: Write Another Extension (csv, txt, json)")
            sys.exit()

    def run(self):
        '''
        main function of this program: 공백단위로 단어를 분리하기, 파일전체에서 “the” 단어가 몇번 나타냈는지 개수 구하기
        :return: nothing
        '''

        propertyData = self.get_property()
        inputData = self.read_data_from_file(propertyData)
        splitByBlankData = self.split_data_by_blank(inputData)
        countOfwords = self.find_count_words(propertyData['word'], splitByBlankData)
        self.write_result_data(propertyData, countOfwords)

        print("Program Run Success!")



if __name__ == "__main__":
    countOfWordsProgram = CountOfWordsProgram()
    countOfWordsProgram.run()