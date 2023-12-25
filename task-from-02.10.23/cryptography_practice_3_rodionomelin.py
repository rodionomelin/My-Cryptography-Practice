#Выполнил: Омелин Р.С.
#Группа: 4Б02 МКН-41

class CaesarCipher:
    def __init__(self, alphabet, shift):
        self.alphabet = alphabet
        self.shift = shift
        self.alpha_len = len(self.alphabet)
        
    def encrypt(self, text):
        encrypted = ''
        for char in text:
            is_upper = char.isupper()
            char = char.upper()
            if char in self.alphabet:
                idx = (self.alphabet.index(char) + self.shift) % self.alpha_len
                encrypted_char = self.alphabet[idx]
                encrypted += encrypted_char if is_upper else encrypted_char.lower()
            else:
                encrypted += char
        return encrypted
    
    def decrypt(self, text):
        decrypted = ''
        for char in text:
            is_upper = char.isupper()
            char = char.upper()
            if char in self.alphabet:
                idx = (self.alphabet.index(char) - self.shift) % self.alpha_len
                decrypted_char = self.alphabet[idx]
                decrypted += decrypted_char if is_upper else decrypted_char.lower()
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
            is_upper = char.isupper()
            char = char.upper()
            if char in alphabet:
                char_index = alphabet.index(char)
                new_char = alphabet[(char_index - shift) % alpha_len]
                decrypted_text += new_char if is_upper else new_char.lower()
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
        is_upper = char.isupper()
        char = char.upper()
        if char in alphabet:
            char_index = alphabet.index(char)
            new_char = alphabet[(char_index - probable_shift) % alpha_len]
            decrypted_text += new_char if is_upper else new_char.lower()
        else:
            decrypted_text += char
    
    return decrypted_text


def frequency_analysis(text, alphabet):

    letter_freq = {letter: 0 for letter in alphabet}

    for char in text:
        if char.upper() in alphabet or char.lower() in alphabet:
            letter_freq[char.upper()] += 1

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

    original_text = '''
Я встретил путника; он шёл из стран далёких
И мне сказал: вдали, где вечность сторожит
Пустыни тишину, среди песков глубоких
Обломок статуи распавшейся лежит.
Из полустёртых черт сквозит надменный пламень,
Желанье заставлять весь мир себе служить;
Ваятель опытный вложил в бездушный камень
Те страсти, что могли столетья пережить.
И сохранил слова обломок изваянья: —
«Я — Озимандия, я — мощный царь царей!
Взгляните на мои великие деянья,
Владыки всех времён, всех стран и всех морей!»
Кругом нет ничего… Глубокое молчанье…
Пустыня мёртвая… И небеса над ней…

Проснитесь и пойте, мистер Фримен. 
Проснитесь и пойте. 
Нет, я не хочу сказать, что Вы спите на работе. 
Никто не заслуживает отдыха больше вашего. 
И все усилия мира пропали бы даром, пока... 
Скажем просто, что Ваш час снова пробил. 
Нужный человек не в том месте может перевернуть мир. 
Так проснитесь же, мистер Фримен. 
Проснитесь, вас снова ждут великие дела.
'''

    print(f"[+] Original: {original_text}")

    encrypted_text = cipher.encrypt(original_text)
    print(f"\n[+] Encrypted: {encrypted_text}")

    decrypted_text = cipher.decrypt(encrypted_text)
    print(f"\n[+] Decrypted: {decrypted_text}")

    cracked_text = crackCaesar(alphabet_ru, ru_freq, encrypted_text)
    print(f"\n[+] Cracked: {cracked_text}")

    freq_ru = frequency_analysis(original_text, alphabet_ru)
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
I met a traveller from an antique land,
Who said—“Two vast and trunkless legs of stone
Stand in the desert. . . . Near them, on the sand,
Half sunk a shattered visage lies, whose frown,
And wrinkled lip, and sneer of cold command,
Tell that its sculptor well those passions read
Which yet survive, stamped on these lifeless things,
The hand that mocked them, and the heart that fed;
And on the pedestal, these words appear:
My name is Ozymandias, King of Kings;
Look on my Works, ye Mighty, and despair!
Nothing beside remains. Round the decay
Of that colossal Wreck, boundless and bare
The lone and level sands stretch far away.

Rise and shine, Mr. Freeman.
Rise and shine...
Not that I wish to imply that you have been sleeping on the job. 
No one is more deserving of a rest, and all the effort in the world would have gone to waste until...
Well... Lets just say your hour has come again.
The right man in the wrong place can make all the difference in the world.
So, wake up Mr. Freeman.
Wake up and... Smell the ashes.
'''

    print(f"\n[+] Original: {original_text}")

    encrypted_text = cipher.encrypt(original_text)
    print(f"\n[+] Encrypted: {encrypted_text}")

    decrypted_text = cipher.decrypt(encrypted_text)
    print(f"\n[+] Decrypted: {decrypted_text}")

    cracked_text = crackCaesar(alphabet_en, en_freq, encrypted_text)
    print(f"\n[+] Cracked: {cracked_text}")

    freq_en = frequency_analysis(original_text, alphabet_en)
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