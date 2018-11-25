#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', family='DejaVu Sans')

import re
import codecs


# значит сперва читаем из файла, считаем количество слов
file = codecs.open('karenina.txt', encoding='utf-8', mode='r')
data = file.read()
file.close()
source_words=re.findall('(\w+)|\n\n+|[.?!]',data,re.UNICODE)
print('------------------1--------------------')
print('Список слов:',source_words[:10])
print('Всего слов, включая концы предложений:',len(source_words))


# потом выбираем уникальные слова из всех. 
# Количество предложений. Предложения разделены пустой строкой
# Ну и частота там из библиотеки сама считается
from collections import Counter
all_words=Counter(source_words)
number_of_sentences=all_words.pop('',None)
print('------------------2--------------------')
print('Всего предложений:',number_of_sentences)
print('Всего различных слов:',len(all_words))
print('Самые часто встречающиеся слова:',all_words.most_common(10))

# тут короче магия магия фигакс
# объединили в массив слов в предложении
# первое слово с залавной буквы. Поэтому фигачим его в ловер кэйс (Если это не что то вроде Анна, крч все бет тут норм)
import itertools
sentences=[list(y) for x, y in itertools.groupby(source_words, lambda z: z == '') if not x]
for sentence in sentences:
    first_word_lower_case=sentence[0].lower()
    if first_word_lower_case in all_words: sentence[0]=first_word_lower_case
print('------------------3--------------------')
print('Начало текста:',sentences[:6])

# Вот там магия была. Потому теперь количество слов уменьшилось. 
# Ведь теперь Слюнявчик и слюнявчик - это одно и то же слово
# Но что произошло с предложениями?? почему их меньше
# Варианты? 
all_words=Counter([word for sentence in sentences for word in sentence])
number_of_sentences=len(sentences)
print('------------------4--------------------')
print('Всего предложений:',number_of_sentences)
print('Всего различных слов:',len(all_words))
print('Самые часто встречающиеся слова:',all_words.most_common(10))


# Убираем редкие и суперчастые слова опять магией питона
least_count=50
max_count=10000
common_words={k: v for k, v in all_words.items() if v>=least_count and v<=max_count}
print('------------------5--------------------')
print('Число встречающихся минимум',least_count,'и максимум',max_count,"раз слов:",len(common_words))


# Сопоставим теперь словам числовые значения: 
# самое частое слово будет иметь значение 0, следующее за ним по частоте значение 1, и т.д. о магия
words_sorted_by_frequency=list(map(lambda x: x[0], sorted(common_words.items(), key=lambda x: -x[1])))
words_codes=dict([(w,c) for c,w in enumerate(words_sorted_by_frequency)])
# эти коллекции можно использовать для сопоставления словам чисел и обратно
print('------------------6--------------------')
print(words_sorted_by_frequency[words_codes['ты']], '-', words_codes['ты'])
print(words_sorted_by_frequency[words_codes['дом']], '-', words_codes['дом'])
print(words_sorted_by_frequency[words_codes['Анна']], '-', words_codes['Анна'])
print(words_sorted_by_frequency[words_codes['что']], '-', words_codes['что'])

# Теперь заменим в тексте все слова ни их коды для ускорения дальнейшей работы. 
# Редкие слова будут просто отброшены из текста.
encoded_text=[[words_codes[word] for word in sentence if word in words_codes] for sentence in sentences]
# убираем пустые предложения меньше заданной длины
minimal_length=4
encoded_text=[sentence for sentence in encoded_text if len(sentence)>=minimal_length]
print('------------------7--------------------')
print('Начало закодированного текста:', encoded_text[:6])
print('Число предложений:', len(encoded_text))

# Для удобства определим функцию, которая будет преобразовывать закодированный текст в читаемый.
def decode(txt):
    return words_sorted_by_frequency[txt] if isinstance(txt,(int,np.integer)) else list(map(decode, list(txt)))
print('------------------8--------------------')
print('Раскодированное начало:', decode(encoded_text[:6]))

# создадим функцию, которая будет возвращать случайный контекст из текста. 
# Максимальное расстояние между словами в контексте передаем в качестве параметра.
def random_context(text, distance_between_words=5):
    random_sentence=text[np.random.randint(0,len(text))]
    word_index=np.random.randint(0,len(random_sentence))
    word=random_sentence[word_index]
    left_context=random_sentence[max(0,word_index-distance_between_words):word_index]
    right_context=random_sentence[(word_index+1):min(len(random_sentence),word_index+distance_between_words)]
    print('Случайный контекст со словом:', decode(left_context+[word]+right_context))
    return word, left_context+right_context
print('------------------9--------------------')
print('Случайный контекст:', decode(random_context(encoded_text, 2)))






















print('-----------------END-------------------')