from oracle_python_v1_2 import pad_oracle
import sys
import codecs

def oracle_attack(c0, c1, checkNum):
    for i in range(256):
        num = format(i, 'x')
        if(len(num) == 1):
            c0 = c0[:18-(2*checkNum)] + '0' + num + c0[20-(2*checkNum):]
        else:
            c0 = c0[:18-(2*checkNum)] + num + c0[20-(2*checkNum):]
        ret_pad = pad_oracle(c0, c1)
        retpad = str(ret_pad)
        if(retpad[2] != '0'):
            return c0

def xorFunc(block, num):
    number = int(block, 16)
    xor = num ^ number
    xor = format(xor, 'x')
    if len(xor) == 1:
        xor = '0' + xor
    return xor

def main():
    # 인자값 없으면 return 0
    if len(sys.argv) != 3:
        print('Please Enter C0 and C1')
        print('Format : $python p_S#.py C0 C1')
        return 0

    # c0, c1 선언
    c0 = sys.argv[1]
    c1 = sys.argv[2]

    # 마지막 block bruteforce attack
    IV = '0x0000000000000000'
    IV = oracle_attack(IV, c1, 1)

    # 확정되는 값
    IV_P = '0x0000000000000000'

    for i in range(8):
        # 1. xor 계산을 통해 IV ⊕ Plaintext 값을 알아낸다 -> 확정되는 값
        # 순서는 for문이 늘어날 때마다 16진수가 0x01부터 1씩 늘어남
        # 따라서 0x01 -> 0x02 0x02 -> 0x03 0x03 0x03 -> ... 순서로 진행
        # (IV ⊕ Plaintext) ⊕ IV = Plaintext
        # (IV ⊕ Plaintext) = Plaintext ⊕ IV
        num = i + 1
        block = IV[18 - (2 * num):20 - (2 * num)]
        xor = xorFunc(block, num)
        IV_P = IV_P[:18 - (2 * num)] + xor + IV_P[20 - (2 * num):]

        if i == 7:
            break

        # 2. padding이 되는 IV 값 구하기
        for k in range(num):
            block = IV_P[18-(2*(k+1)):20-(2*(k+1))]
            # # 위의 IV_P에서 0x01 padding이 되었다면 이번엔 0x02(+0x01)와 padding해야 함
            xor = xorFunc(block, num+1)
            IV = IV[:18-(2*(k+1))] + xor + IV[20-(2*(k+1)):]

        # 3. 다음 계산을 위해 다음 padding을 적용한 IV로 변환
        IV = oracle_attack(IV, c1, num+1)

    print('---------------------------')
    print(f'IV_P : {IV_P}')
    print(f'IV : {IV}')
    print(f'first IV : {c0}')
    print('---------------------------')

    Plaintext = '0x'

    # IV ⊕ IV ⊕ Plaintext = 0 ⊕ Plaintext = Plaintext
    # IV는 처음 입력 받았던 c0
    for i in range(8):
        num = i + 1
        block1 = c0[2 * num:2 * num + 2]
        block2 = IV_P[2 * num:2 * num + 2]
        number2 = int(block2, 16)
        xor = xorFunc(block1, number2)
        Plaintext = Plaintext + xor

    asciiPlaintext = ""
    for i in range(1, 9):
        block = Plaintext[18-(2*i):20-(2*i)]
        number = int(block, 16)
        if number <= 8:
            continue
        else:
            binary_str = codecs.decode(block, "hex")
            asciiPlaintext = str(binary_str, "utf-8") + asciiPlaintext

    print(f'Result Plaintext : {asciiPlaintext}')

    return 0

if __name__ == "__main__":
    main()