print(f"\n[+] Frequencies:")
    for letter, frequency in freq_ru.items():
        if frequency > 0:
            print(f"{letter}: {frequency:.2f}%")