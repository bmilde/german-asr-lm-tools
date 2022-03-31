from normalisierung import num2text

# NumberFormatter can format German ASR output that contains numbers:
#
# E.g. drei hundert neun und neuzig -> dreihundertneunundneuzig
#
# or drei hundert neun und neuzig -> 399 if convert_to_numbers=True (default)
#
# example usage for numbers 7 to 100000, with years:
#
# nf = NumberFormatter(min_num=7, max_num=100000, with_centuries=True)
# example = nf.normalize_text("Der Zug Nummer vier hundert neun und neunzig fährt ein".split())
# -> ['Der', 'Zug', 'Nummer', '499', 'fährt', 'ein'] 

def ngrams(input_list, n):
# from https://stackoverflow.com/questions/17531684/n-grams-in-python-four-five-six-grams
    if n<=1:
        return [[elem] for elem in input_list]
    return zip(*[input_list[i:] for i in range(n)])

def num2text_lower(str_num):
    return num2text(str_num).replace(' ','').lower()

class NumberFormatter:    
    def __init__(self, min_num=7, max_num=100000, max_case_num=10000, with_centuries=True, debug_prints=False):
        self.numbers = {}

        for num in range(1, max_num):
            str_num = str(num)
            num_text = num2text_lower(str_num)
            if num >= min_num:
                self.numbers[num_text] = str_num
            if debug_prints:
                print(num_text)
            if num < 20:
                self.numbers[num_text+'te'] = str_num + '.'
                self.numbers[num_text+'ten'] = str_num + '.'
                self.numbers[num_text+'ter'] = str_num + '.'
                self.numbers[num_text+'tem'] = str_num + '.'
            elif num >= 20 and num <= max_case_num:
                self.numbers[num_text+'ste'] = str_num + '.'
                self.numbers[num_text+'sten'] = str_num + '.'
                self.numbers[num_text+'ster'] = str_num + '.'
                self.numbers[num_text+'stem'] = str_num + '.'

        if with_centuries:
            for century in range(12,20):
                for year in range(0,100):
                    str_year = num2text_lower(str(century)) + 'hundert' + num2text_lower(str(year))
                    self.numbers[str_year] = century*100+year
                    if debug_prints:
                        print(str_year, century*100+year)

    def normalize_text(self, token_list, convert_to_numbers=True, debug_prints=False):
        token_list_tmp = token_list
        for n in range(8,0,-1):
            token_list_tmp2 = []
            jump_tokens = 0
            for elem in ngrams(token_list_tmp, n):
                if debug_prints:
                    print(elem, token_list_tmp2)
                test_num = ''.join(elem).lower()
                if debug_prints:
                    print(test_num)
                if test_num in self.numbers:
                    if debug_prints:
                        print(test_num,self.numbers[test_num])
                    if convert_to_numbers:
                        token_list_tmp2.append(str(self.numbers[test_num]))
                    else:
                        token_list_tmp2.append(test_num)
                    jump_tokens = n-1
                else:
                    if jump_tokens == 0:
                        token_list_tmp2.append(elem[0])
                    else:
                        jump_tokens -= 1
            if n > 1 and n-1-jump_tokens > 0:
                if debug_prints:
                    print('jump_tokens',jump_tokens,'n',n,'add: ', token_list_tmp[-(n-1-jump_tokens):])
                token_list_tmp2 += token_list_tmp[-(n-1-jump_tokens):]
            token_list_tmp = token_list_tmp2
            if debug_prints:
                print(token_list_tmp)

        return token_list_tmp

if __name__ == '__main__':

    nf = NumberFormatter()

    print(num2text("499"))            
    print(nf.numbers["vierhundertneunundneunzig"])
    print(nf.numbers["neunzehnhundertneunundneunzig"])
    test = nf.normalize_text("drei tausend Dollar liegen rum und ein Hundert vierzehn Euro.".split()) 
    print(test)
    test = nf.normalize_text("Der Zug Nummer vier hundert neun und neunzig fährt ein".split(), convert_to_numbers=False) 
    print(test)
    test = nf.normalize_text("Der Zug Nummer vier hundert neun und neunzig fährt ein".split()) 
    print(test)
    test = nf.normalize_text("Drei Hundert einundsiebzig Frauen und vier Hundert zweiundneunzig Männer sind ...".split()) 
    print(test)
    test = nf.normalize_text("er ist drei und sechzig".split())
    print(test)
    test = nf.normalize_text("neun zehn hundert neun und neunzig".split())
    print(test)
    test = nf.normalize_text("am zwei und zwanzigsten Mai neun zehn hundert neun und neunzig".split())
    print(test)

    test = nf.normalize_text("am sechsten Mai neun zehn hundert neun und neunzig".split())
    print(test)
