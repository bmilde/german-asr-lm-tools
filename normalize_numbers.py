from normalisierung import num2text

# from https://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams
def ngrams(input_list, n):
    if n<=1:
        return [[elem] for elem in input_list]
    return zip(*[input_list[i:] for i in range(n)])

def num2text_lower(str_num):
    return num2text(str_num).replace(' ','').lower()

numbers = {}

for num in range(7,100000):
    str_num = str(num)
    num_text = num2text_lower(str_num)
    numbers[num_text] = num
#    print(num_text)

for century in range(12,20):
    for year in range(0,100):
        str_year = num2text_lower(str(century)) + 'hundert' + num2text_lower(str(year))
        numbers[num_text] = century*100+year
#        print(str_year, century*100+year)

def normalize_text(token_list,convert_to_numbers=True):
    token_list_tmp = token_list
    for n in range(8,0,-1):
        token_list_tmp2 = []
        jump_tokens = 0
        for elem in ngrams(token_list_tmp, n):
#            print(elem)
            if convert_to_numbers:
                test_num = ''.join(elem).lower()
#                print(test_num)
                if test_num in numbers:
#                    print(test_num,numbers[test_num])
                    token_list_tmp2.append(str(numbers[test_num]))
                    jump_tokens = n-1
                else:
                    if jump_tokens == 0:
                        token_list_tmp2.append(elem[0])
                    else:
                        jump_tokens -= 1
        if n > 1:
            token_list_tmp2 += token_list_tmp[-(n-1-jump_tokens):]
        token_list_tmp = token_list_tmp2
#        print(token_list_tmp)

    return token_list_tmp

if __name__ == '__main__':
    print(num2text("499"))            
    print(numbers["vierhundertneunundneunzig"])
    test = normalize_text("drei tausend Dollar liegen rum und vierzehn Euro.".split()) 
    print(test)
    test = normalize_text("Der Zug Nummer vier hundert neun und neunzig fährt ein".split()) 
    print(test)
    test = normalize_text("Drei Hundert einundsiebzig Frauen und vier Hundert zweiundneunzig Männer sind ...".split()) 
    print(test)
