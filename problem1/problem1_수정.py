from tkinter import *
import pandas as pd
import yaml


class Remove_Special_Character_Program:

    def __init__(self):
        pass

    def input_remove_specialCharacter(self, text, sc):
        '''
        get input punctuation and remove them
        :param text: text data with dataframe type
        :param sc: special characters getting from input
        :return:text with no special characters
        '''

        sc += '\n'
        no_sc = "".join([c for c in text if c not in sc])
        return no_sc

    def replace_specialCharacter(self, text):
        '''
        replace special character to spacebar character
        :param text: text data with dataframe type
        :return: text with replacing special characters to spacebar character
        '''

        no_sc = re.sub(r'[^\w\s]', ' ', text)
        no_sc = re.sub(r'\_', ' ', no_sc)
        no_sc = re.sub(r'\n', '', no_sc)

        return no_sc

    def split_data(self, rawData):
        '''
        get document number & remove doc number in text
        :param rawData: data from file
        :return: data converted to dataframe type
        '''

        fNum = []
        index = 0
        for line in rawData:
            if line.split(' ')[0].isdigit() == True:
                fNum.append(int(line.split(' ')[0]))
                rawData[index] = line.replace(line.split(' ')[0], '')
                index += 1

        data = {'docNum': fNum, 'text': rawData}
        data = pd.DataFrame(data)

        return data

    def text_processing(self, propertyData, data):
        '''
        text processing function (remove special characters from data)
        :param propertyData: data from property file
        :param data: data with dataframe type
        :return: 'processed data', 'output file name'
        '''

        scOption = propertyData['option']
        if (scOption == 'replace'):
            specialChar = propertyData['special characters']
            outputFileName = propertyData['output']
            data['text'] = data['text'].apply(lambda x: self.input_remove_specialCharacter(x, specialChar))
        elif (scOption == 'remove'):
            outputFileName = propertyData['output']
            data['text'] = data['text'].apply(lambda x: self.replace_specialCharacter(x))
        else:
            print("\'option\'에 \'remove\' (이)나 \'replace\' 를 입력해야합니다.")
            sys.exit()

        return data, outputFileName

    def get_data(self, propertyData):
        '''
        get data from input file using property data
        :param propertyData: data from property file
        :return: data from input file
        '''
        try:
            fileName = propertyData['input']
        except IndexError as e:
            print("property 파일에 input을 써주세요:{}".format(e))
        try:
            with open(fileName, 'r') as file:
                dataFromFile = file.readlines()
        except FileNotFoundError as e:
            print('해당하는 파일이 없습니다: {}.format'.format(e))

        return dataFromFile

    def get_property(self):
        '''
        get data from property file
        :return: data from property file
        '''

        try:
            with open("property.yml") as file:
                propertyData = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            print('해당하는 파일이 없습니다: {}'.format(e))

        return propertyData

    def write_data(self, data, outFName):
        '''
        output file name and extension option to save results by extension option
        :param data: results that have to save
        :return: nothing
        '''

        fn = outFName.split('.')[0]
        ext = outFName.split('.')[1]

        if (ext == "csv"):  # result to csv
            data.to_csv(fn + '.csv', index=False, header=['docNum', 'text'])
        elif (ext == "txt"):    # result to txt
            fn = fn + '.txt'
            with open(fn, 'w') as f:
                f.write(data.to_string(header=False, index=False))
        elif (ext == "json"):   # result to json
            fn = fn + '.json'
            data.to_json(fn, orient='table')
        else:
            print("Error: Write Another Extension (csv, txt, json)")
            self.write_data(data, outFName)

    def run(self):
        '''
        main function of this program: 문자열에서 영문, 숫자를 제외한 문자열 제거하기
        :return: nothing
        '''

        propertyData = self.get_property()
        dataFrame = self.get_data(propertyData)
        data = self.split_data(dataFrame)
        processedData, outputFileName = self.text_processing(propertyData, data)
        self.write_data(processedData, outputFileName)

        print("Program Run Success!")


if __name__ == "__main__":
    removeSpecialCharacterProgram = Remove_Special_Character_Program()
    removeSpecialCharacterProgram.run()