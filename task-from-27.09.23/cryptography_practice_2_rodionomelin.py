#Выполнил: Омелин Р.С.
#Группа: 4Б02 МКН-41

class VigenereCipher:
    def __init__(self, alphabet, key):
        self.alphabet = alphabet
        self.key = key

    def encrypt(self, text):
        key_extended = self._extend_key(text)
        encrypted_text = ''
        for t, k in zip(text, key_extended):
            index = (self.alphabet.index(t) + self.alphabet.index(k)) % len(self.alphabet)
            encrypted_text += self.alphabet[index]
        return encrypted_text

    def decrypt(self, encrypted_text):
        key_extended = self._extend_key(encrypted_text)
        decrypted_text = ''
        for e, k in zip(encrypted_text, key_extended):
            index = (self.alphabet.index(e) - self.alphabet.index(k)) % len(self.alphabet)
            decrypted_text += self.alphabet[index]
        return decrypted_text

    def _extend_key(self, text):
        key_extended = ''
        while len(key_extended) < len(text):
            key_extended += self.key
        return key_extended[:len(text)]

class BlockPermutationCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, text):
        encrypted_text = ''
        for i in range(0, len(text), len(self.key)):
            block = text[i:i + len(self.key)]
            for k in self.key:
                if k - 1 < len(block):
                    encrypted_text += block[k - 1]
        return encrypted_text

    def decrypt(self, encrypted_text):
        decrypted_text = ''
        inverted_key = [0] * len(self.key)
        for i, k in enumerate(self.key):
            inverted_key[k - 1] = i + 1

        for i in range(0, len(encrypted_text), len(self.key)):
            block = encrypted_text[i:i + len(self.key)]
            for j in range(len(block)):
                position = inverted_key[j] - 1
                decrypted_text += block[position]
        return decrypted_text
    
#Tasks
def task1():
    # Task 1
    print('\n[+] Задание 1')

    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    key = 'СТАКАН'
    text1 = 'КРИПТОСТОЙКОСТЬ'
    text2 = 'ГАММИРОВАНИЕ'

    cipher = VigenereCipher(alphabet, key)

    print('Зашифрованный текст:')
    print(f'1) "{text1}": {cipher.encrypt(text1)}')
    print(f'2) "{text2}": {cipher.encrypt(text2)}')

def task2():
    # Task 2
    print('\n[+] Задание 2')

    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_'
    key = 'ОРЕХ'
    encrypted_text1 = 'ШВМБУЖНЯ'
    encrypted_text2 = 'ЯБХЪШЮМХ'

    cipher = VigenereCipher(alphabet, key)

    print('Расшифрованный текст:')
    print(f'1) "{encrypted_text1}": {cipher.decrypt(encrypted_text1)}')
    print(f'2) "{encrypted_text2}": {cipher.decrypt(encrypted_text2)}')

def task3():
    # Task 3
    print('\n[+] Задание 3')

    key = [4, 3, 6, 2, 1, 5]
    text1 = 'ОТСТУПАЙ_ВРАГ_РЯДОМ'
    text2 = 'УБИРАЙ_ДОКУМЕНТЫ'

    cipher = BlockPermutationCipher(key)

    print('Зашифрованный текст:')
    print(f'1) "{text1}": {cipher.encrypt(text1)}')
    print(f'2) "{text2}": {cipher.encrypt(text2)}')

def task4():
    # Task 4
    print('\n[+] Задание 4')

    key = [6, 4, 2, 7, 5, 8, 1, 3]
    encrypted_text1 = 'СЛПИЬНАЕ'
    encrypted_text2 = 'РОИАГДВН'

    cipher = BlockPermutationCipher(key)

    print('Расшифрованный текст:')
    print(f'1) "{encrypted_text1}": {cipher.decrypt(encrypted_text1)}')
    print(f'2) "{encrypted_text2}": {cipher.decrypt(encrypted_text2)}')

def main():
    print('Выполнил: Омелин Р.С.')
    print('Группа: 4Б02 МКН-41')

    task1()
    task2()
    task3()
    task4()

if __name__ == '__main__':
    main()