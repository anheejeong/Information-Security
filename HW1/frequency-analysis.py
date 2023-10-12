import re
import collections

def word_freq(ciphertext):
    # Select only the alphabet
    chartext = re.sub(r'[^a-zA-Z]', '', ciphertext)
    # Number of occurrences of each alphabet
    wordfrequency = collections.Counter(chartext)
    return wordfrequency

def most_freq_two(wordfrequency, alphabet):
    # Extract the two most frequent alphabets
    most_common_elements = wordfrequency.most_common(2)
    first = ""
    second = ""
    for element, count in most_common_elements:
        if first == "":
            first = first + element
        else:
            second = second + element
    alphabet[first] = 'e'
    alphabet[second] = 't'
    return first, second

def decrypt(ciphertext, first, second, plaintext): # e, t
    for idx, val in enumerate(ciphertext):
        if val == first:
            plaintext = plaintext[:idx] + "e" + plaintext[idx+1:]
        elif val == second:
            plaintext = plaintext[:idx] + "t" + plaintext[idx+1:]
    return plaintext

def second_decrypt(ciphertext, plaintext, keyword, alphabet):
    findkeyword = ""
    changeword1 = ""
    changeword2 = ""
    reverse_dict = dict(map(reversed, alphabet.items()))
    for val in keyword:
        if val in reverse_dict:
            findkeyword = findkeyword + val
        else:
            findkeyword = findkeyword + "*"
            if not changeword1:
                changeword1 = changeword1 + val
            else:
                changeword2 = changeword2 + val
    # '*' make no more than three so a maximum of two
    ox = plaintext.find(findkeyword)
    if ox != -1:
        findword1 = ""
        findword2 = ""
        for idx, val in enumerate(findkeyword):
            if val == '*':
                if not findword1:
                    findword1 = ciphertext[ox + idx]
                    alphabet[findword1] = changeword1
                else:
                    findword2 = ciphertext[ox + idx]
                    alphabet[findword2] = changeword2

        for idx, val in enumerate(ciphertext):
            if val == findword1:
                plaintext = plaintext[:idx] + changeword1 + plaintext[idx + 1:]
            elif val == findword2:
                plaintext = plaintext[:idx] + changeword2 + plaintext[idx + 1:]
    return plaintext


def main():
    alphabet = {
        'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0,
        'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0,
        'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0
    }
    # ciphertext = "Uz qso vuohxmopv gpozpevsg zwsz opfpesx udbmetsx aiz vuephz hmdzshzo wsfp appd tsvp quzw ymxuzuhsx epyepopdzszufpo mb zwp fupz hmdj ud tmohmq."
    ciphertext = "Zbzvepiz uaywpaz upa pbxpah nboarbuv upyu taxyuaz upa xqoz yto hybzaz hqwcz. " \
                 "Pa uqq wqtwrioaz upyu yrr bz larr. " \
                 "Upbz itbmahza tql lbupqiu y jyzuah zaajz uq pbj tabupah zuahbra tqh nahubra. " \
                 "Aywp yuqj qn upyu zuqta, aywp jbtahyr nryca qn upbz jqituybt nirr qn tbxpu, yrqta nqhjz y lqhro. " \
                 "Upa zuhixxra buzarn uq upa pabxpuz bz atqixp uq nbrr y jyt'z payhu. " \
                 "Qta jizu bjyxbta Zbzvepiz pyeev."
    ciphertext = ciphertext.lower()
    wordfrequency = word_freq(ciphertext)
    first, second = most_freq_two(wordfrequency, alphabet)

    plaintext = ""
    for idx, val in enumerate(ciphertext):
        if val == " ":
            plaintext = plaintext + " "
        elif val == ".":
            plaintext = plaintext + "."
        elif val == ",":
            plaintext = plaintext + ","
        elif val == "'":
            plaintext = plaintext + "'"
        else :
            plaintext = plaintext + "*"

    plaintext = decrypt(ciphertext, first, second, plaintext) # t, e

    keyword = ["the", "that", "it", "this", "too", "have", "been", "with", "was", "neither", "but", "several", "direct", "disclosed", "teaches", "raises", "political", "itself", "of", "informal", "cong", "yesterday", "higher", "imagine", "without", "universe", "and", "fidelity","flake", "happy"]
    for i in keyword:
        plaintext = second_decrypt(ciphertext, plaintext, i, alphabet)

    print(f'\nCIPHERTEXT : {ciphertext}\n')
    print('=>')
    print(f'\nPLAINTEXT : {plaintext} \n')
    print(f'FREQUENCY : {wordfrequency}\n')
    print(f'KEY : {alphabet}\n')
    print('***Ignore capital letters***')
    print('***Alphabet with value 0 in dictionary is unknown because it never comes from ciphertext***\n')

if __name__ == "__main__":
    main()