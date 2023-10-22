#Выполнил: Омелин Р.С.
#Группа: 4Б02 МКН-41

class GOST_28147_89(object):
    def __init__(self, key, sbox):
        self._key = key
        self._subkeys = [(key >> (32 * i)) & 0xFFFFFFFF for i in range(8)]
        self.sbox = sbox

    def encrypt_round(self, part, key):
        temp = part ^ key 
        output = 0

        for i in range(8):
            output |= ((self.sbox[i][(temp >> (4 * i)) & 0b1111]) << (4 * i))

        return ((output >> 11) | (output << (32 - 11))) & 0xFFFFFFFF

    def encrypt(self, text):

        left_part = text >> 32
        right_part = text & 0xFFFFFFFF

        for i in range(24):
            left_part, right_part = right_part, left_part ^ self.encrypt_round(right_part, self._subkeys[i % 8])

        for i in range(8):
            left_part, right_part = right_part, left_part ^ self.encrypt_round(right_part, self._subkeys[7 - i])

        return (left_part << 32) | right_part

    def decrypt(self, text):
        left_part = text >> 32
        right_part = text & 0xFFFFFFFF

        for i in range(8):
            left_part, right_part = right_part ^ self.encrypt_round(left_part, self._subkeys[i]), left_part

        for i in range(24):
            left_part, right_part = right_part ^ self.encrypt_round(left_part, self._subkeys[(7 - i) % 8]), left_part

        return (left_part << 32) | right_part

#Задание от 09.10
def main():
    print('Выполнил: Омелин Р.С.')
    print('Группа: 4Б02 МКН-41')

    sbox = (
        (4, 2, 15, 5, 9, 1, 0, 8, 14, 3, 11, 12, 13, 7, 10, 6),
        (12, 9, 15, 14, 8, 1, 3, 10, 2, 7, 4, 13, 6, 0, 11, 5),
        (13, 8, 14, 12, 7, 3, 9, 10, 1, 5, 2, 4, 6, 15, 0, 11),
        (14, 9, 11, 2, 5, 15, 7, 1, 0, 13, 12, 6, 10, 4, 3, 8),
        (3, 14, 5, 9, 6, 8, 0, 13, 10, 11, 7, 12, 2, 1, 15, 4),
        (8, 15, 6, 11, 1, 9, 12, 5, 13, 3, 7, 10, 0, 14, 2, 4),
        (9, 11, 12, 0, 3, 6, 7, 5, 4, 8, 14, 15, 1, 10, 2, 13),
        (12, 6, 5, 2, 11, 0, 9, 13, 3, 14, 7, 10, 15, 4, 1, 8),
    )
    
    text = '''
Проснитесь и пойте, мистер Фримен. 
Проснитесь и пойте. 
Нет, я не хочу сказать, что Вы спите на работе. 
Никто не заслуживает отдыха больше вашего. 
И все усилия мира пропали бы даром, пока... 
Скажем просто, что Ваш час снова пробил. 
Нужный человек не в том месте может перевернуть мир. 
Так проснитесь же, мистер Фримен.
Проснитесь, вас снова ждут великие дела.'''
    
    import random
    key = 0
    for _ in range(32):
        key = (key << 8) | random.randint(0, 255)

    print(f"\n[+] Key:  {key}")

    text_bytes = text.encode('utf-8')
    text_number = int.from_bytes(text_bytes, byteorder='big')

    gost = GOST_28147_89(key, sbox)

    encrypted_text = gost.encrypt(text_number)

    decrypted_text = gost.decrypt(encrypted_text)
    decrypted_text_bytes = decrypted_text.to_bytes((decrypted_text.bit_length() + 7) // 8, byteorder='big')
    decrypted_text_str = decrypted_text_bytes.decode('utf-8')

    print(f"\n[+] Original Text:  {text}")

    print(f"\n[+] Encrypted Text: {encrypted_text}")

    print(f"\n[+] Decrypted Text: {decrypted_text_str}")

if __name__ == "__main__":
    main()