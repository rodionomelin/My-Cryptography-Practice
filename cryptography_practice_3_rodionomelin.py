#Выполнил: Омелин Р.С.
#Группа: 4Б02 МКН-41

class CaesarCipher:
    def __init__(self, alphabet,  shift):
        self.alphabet = alphabet
        self.shift = shift
        self.alpha_len = len(self.alphabet)
        
    def encrypt(self, text):
        encrypted = ''
        for char in text:
            if char in self.alphabet:
                idx = (self.alphabet.index(char) + self.shift) % self.alpha_len
                encrypted += self.alphabet[idx]
            else:
                encrypted += char
        return encrypted
    
    def decrypt(self, text):
        decrypted = ''
        for char in text:
            if char in self.alphabet:
                idx = (self.alphabet.index(char) - self.shift) % self.alpha_len
                decrypted += self.alphabet[idx]
            else:
                decrypted += char
        return decrypted

def crackCaesar(alphabet, freq, text):

    alpha_len = len(alphabet)
    
    max_corr = -1
    probable_shift = 0
    
    for shift in range(alpha_len):
        decrypted_text = ""

        for char in text:
            if char in alphabet:
                char_index = alphabet.index(char)
                decrypted_text += alphabet[(char_index - shift) % alpha_len]
            else:
                decrypted_text += char
        
        letter_freq = [0] * alpha_len
        total_letters = 0
        
        for char in decrypted_text:
            if char in alphabet:
                idx = alphabet.index(char)
                letter_freq[idx] += 1
                total_letters += 1
        
        correlation = 0
        
        for i in range(alpha_len):
            correlation += (letter_freq[i] / total_letters) * (freq[i] / 100)
        
        if correlation > max_corr:
            max_corr = correlation
            probable_shift = shift
    
    decrypted_text = ""
    for char in text:
        if char in alphabet:
            char_index = alphabet.index(char)
            decrypted_text += alphabet[(char_index - probable_shift) % alpha_len]
        else:
            decrypted_text += char
    
    return decrypted_text


def frequency_analysis(text, alphabet):
    letter_freq = {letter: 0 for letter in alphabet}
    total_letters = 0
    
    for char in text:
        if char in alphabet:
            letter_freq[char] += 1
            total_letters += 1
    
    for letter, count in letter_freq.items():
        letter_freq[letter] = (count / total_letters) * 100
        
    return letter_freq

def task1():
    print('\nПример с Русским языком')
    alphabet_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    ru_freq = [
            8.01, 1.59, 4.54, 1.70, 2.98, 8.45, 0.04, 0.94, 1.65, 7.35,
            1.21, 3.49, 4.40, 3.21, 6.70, 10.97, 2.81, 4.73, 5.47, 6.26,
            2.62, 0.26, 0.97, 0.48, 1.44, 0.73, 0.36, 0.04, 1.90, 1.74,
            0.32, 0.64, 2.01
        ]
    
    shift = 3

    cipher = CaesarCipher(alphabet_ru, shift)

    original_text = "ПРИМЕРШИФРОТЕКСТА"
    print(f"[+] Original: {original_text}")

    encrypted_text = cipher.encrypt(original_text)
    print(f"\n[+] Encrypted: {encrypted_text}")

    decrypted_text = cipher.decrypt(encrypted_text)
    print(f"\n[+] Decrypted: {decrypted_text}")

    cracked_text = crackCaesar(alphabet_ru, ru_freq, encrypted_text)
    print(f"\n[+] Cracked: {cracked_text}")

    freq_ru = frequency_analysis(encrypted_text, alphabet_ru)
    print(f"\n[+] Frequencies:")
    for letter, frequency in freq_ru.items():
        if frequency > 0:
            print(f"{letter}: {frequency:.2f}%")
    



def task1_1():
    print('\nПример с Английским языком')
    alphabet_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    en_freq = [
        8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15,
        0.77, 4.0, 2.4, 6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1,
        2.8, 0.98, 2.4, 0.15, 2.0, 0.074
    ]
    shift = 11

    cipher = CaesarCipher(alphabet_en, shift)

    original_text = '''
I MET A TRAVELLER FROM AN ANTIQUE LAND,
WHO SAID—“TWO VAST AND TRUNKLESS LEGS OF STONE
STAND IN THE DESERT. . . . NEAR THEM, ON THE SAND,
HALF SUNK A SHATTERED VISAGE LIES, WHOSE FROWN,
AND WRINKLED LIP, AND SNEER OF COLD COMMAND,
TELL THAT ITS SCULPTOR WELL THOSE PASSIONS READ
WHICH YET SURVIVE, STAMPED ON THESE LIFELESS THINGS,
THE HAND THAT MOCKED THEM, AND THE HEART THAT FED;
AND ON THE PEDESTAL, THESE WORDS APPEAR:
MY NAME IS OZYMANDIAS, KING OF KINGS;
LOOK ON MY WORKS, YE MIGHTY, AND DESPAIR!
NOTHING BESIDE REMAINS. ROUND THE DECAY
OF THAT COLOSSAL WRECK, BOUNDLESS AND BARE
THE LONE AND LEVEL SANDS STRETCH FAR AWAY.
'''

    print(f"\n[+] Original: {original_text}")

    encrypted_text = cipher.encrypt(original_text)
    print(f"\n[+] Encrypted: {encrypted_text}")

    decrypted_text = cipher.decrypt(encrypted_text)
    print(f"\n[+] Decrypted: {decrypted_text}")

    cracked_text = crackCaesar(alphabet_en, en_freq, encrypted_text)
    print(f"\n[+] Cracked: {cracked_text}")

    freq_en = frequency_analysis(encrypted_text, alphabet_en)
    print(f"[+] Frequencies:")
    for letter, frequency in freq_en.items():
        if frequency > 0:
            print(f"{letter}: {frequency:.2f}%")

#Задание от 02.10
def main():
    print('Выполнил: Омелин Р.С.')
    print('Группа: 4Б02 МКН-41')

    task1()
    task1_1()

if __name__ == '__main__':
    main()