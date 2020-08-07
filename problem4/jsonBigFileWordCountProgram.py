import csv
import sys
import time
from collections import Counter

import pandas as pd
import yaml


class JsonFileWordCountProgram:

    def __init__(self, chunk_size, counted_data):
        self.chunk_size = chunk_size
        self.counted_data = counted_data

    def get_yaml_property(self):
        '''
        yaml 형태의 property 파일을 읽어들임
        :return: object 형태의 데이터
        '''

        with open("property.yml") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        return data

    def get_keydata_divided_by_chunk(self, input_file_name, key):
        '''
        json 파일에서 해당하는 key값에만 해당하는 데이터를 chunk_size만큼 가져와서 yield 처리함
        :param inputFileName: input 파일 이름
        :param key: 가져올 key의 이름
        :return: yield -> key값에만 해당하는 2차원 list 형태의 데이터
        '''

        for chunk in pd.read_json(input_file_name, encoding='utf-8', lines=True, chunksize=self.chunk_size):
            key_data = list(chunk.loc[:, key])
            yield key_data

    def split_data_by_blank(self, data):
        '''
        2차원 list 형태의 input을 공백 단위로 나눠서 2차원 list 형태로 return
        :param raw_data: input 데이터
        :return: 공백으로 나눠진 2차원 list 형태의 데이터
        '''

        for index in range(len(data)):
            data[index] = data[index].split()

        return data

    def update_count_by_word(self, splitted_data):
        '''
        chunk 단위로 나눈 데이터로부터 각 단어의 개수를 셈
        :param splitted_data: 공백 단위로 나눠진 list 형태의 데이터
        :return: the_number_of_word = 파일이 가지고 있는 총 단어의 개수 (set)
        '''

        for i in range(len(splitted_data)):
            self.counted_data.update(splitted_data[i])

        the_number_of_words = len([key for key, value in self.counted_data.items()])

        return the_number_of_words

    def sort_collections_to_list(self, property_data, length):
        '''
        collections 형태의 데이터를 정렬하여 list 형태로 return
        :param property_data: sort option을 선택하기 위한 property data
        :param counted_data: 각 단어가 몇 개 인지 세어진 데이터
        :param length: input 파일이 가지고 있는 총 단어의 개수 (set)
        :return: 내림차순이나 오름차순으로 정렬한 list 형태의 데이터
        '''

        sort_option = property_data['sort option']

        if sort_option == 'descending':
            sorted_list = self.counted_data.most_common(n=length)  # 내림차순
        elif sort_option == 'ascending':
            sorted_list = list(reversed(self.counted_data.most_common(n=length)))  # 오름차순
        else:
            print("Error: property 파일에 적을 수 있는 'sort option' 내림차순과 오름차순입니다. (option: descending, ascending)")
            sys.exit()

        return sorted_list

    def write_result_data(self, property_data, output_data):
        '''
        확장자에 맞게 최종 데이터셋 저장
        :param property_data: 옵션을 선택하기 위한 property data
        :param output_data: 최종적으로 저장할 데이터
        :return: 없음
        '''

        outputFileName = property_data['output']
        try:
            ext = outputFileName.split('.')[1]
        except IndexError as e:
            print("'property' 파일의 'output'에 파일 확장자를 붙여서 적어주시기 바랍니다: {}".format(e))


        if (ext == "csv"):  # csv 파일로 내보내기
            try:
                with open(outputFileName, 'w', encoding='UTF-8-sig', newline="") as file:
                    writer = csv.writer(file)
                    for row in (output_data):
                        writer.writerow(row)
            except PermissionError as e:
                print("해당 CSV파일을 닫아주시기 바랍니다: {}".format(e))
        elif (ext == "txt"):  # txt 파일로 내보내기
            with open(outputFileName, 'w', encoding='UTF-8') as file:
                for c in range(len(output_data)):
                    file.writelines(str(output_data[c][0]) + ' ' + str(output_data[c][1]) + "\n")
        elif (ext == "json"):  # json 파일로 내보내기
            output_data.to_json(outputFileName, orient='table', encoding='UTF-8-sig')
        else:
            print("Error: 해당되는 확장자만 적어주세요. (csv, txt, json)")
            sys.exit()

    def run(self):
        '''
        main function of this program: 단어 개수 출력하기
        :return: 없음
        '''

        now = time.localtime()
        print("[ 프로그램 시작 시간: %04d/%02d/%02d %02d:%02d:%02d ]" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

        start_time = time.time()
        property_data = self.get_yaml_property()
        i = 1
        for key_data_from_json in self.get_keydata_divided_by_chunk(property_data["input"], property_data["key"]):
            split_data = self.split_data_by_blank(key_data_from_json)
            num = self.update_count_by_word(split_data)
            print("{}번째".format(i), end=' ') # 마지막: 28번째
            i += 1
        sorted_list = self.sort_collections_to_list(property_data, num)
        self.write_result_data(property_data, sorted_list)
        end_time = time.time()

        now = time.localtime()
        print("[ 프로그램 종료 시간: %04d/%02d/%02d %02d:%02d:%02d ]" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
        print("- 걸린 시간: {} sec".format(end_time-start_time))



if __name__ == "__main__":
    chunk_size = 20000
    counted_data = Counter()

    jsonFileWordCountProgram = JsonFileWordCountProgram(chunk_size, counted_data)
    jsonFileWordCountProgram.run()