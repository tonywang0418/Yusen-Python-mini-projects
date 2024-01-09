#!/usr/bin/python3
# This script will count the number of vowels and consonants in a text.
# YW-20240109

TEXT = "Yes and No are not the only answers. In the intricate and sometimes perplexing realm of security, the straightforward ‘yes’ and ‘no’ answers we’re accustomed to may suddenly seem elusive. It’s a humorous take on the intricacies of security, where the right answer might be 'Well, it depends,' and navigating the security landscape feels a bit like solving a riddle. Welcome to the world where black and white answers are a rare find and shades of gray are supreme. The majority of security breaches are caused by human error. Even though you send out reminder emails and try to teach everyone the cybersecurity safety practices, because humans are evolved to trust people, someone will always trust the wrong person causing a breach. It’s like trying to teach a goldfish to play fetch. So, while you keep fighting the good fight against digital chaos, you secretly wish that human error would take a vacation."  

def count_vowels(TEXT):
    """The following function is use to count vowels, whenever the script finds one it will +1 """
    TEXT_lower = TEXT.lower() #This is a way to treat captial letter as lowercase letter
    vowels = "aeiou"
    
    vowel_count = 0 

    for letter in TEXT_lower:
        if letter in vowels:
            vowel_count += 1
    
    return vowel_count
def count_consonants(text):
    """The following function is use to count consonants, whenever the script finds one it will +1 """
    TEXT_lower = TEXT.lower()  #This is a way to treat captial letter as lowercase letter
    consonants = "bcdfghjklmnpqrstvwxyz"
    
    consonants_count = 0

    for letter in TEXT_lower:
        if letter in consonants:
            consonants_count += 1

    return consonants_count
def main():
    """I created empty dictionaries for vowels and consonants as required"""
#This is just my orignal script but since the requirement is to have two empty dictionaries so I have to write a new one.
    #vowels = {"letter": ["a", "e", "i", "o", "u"] }
    #consonants = {"letter": ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y"]}
    #count_v = sum(TEXT_lower.count(letter) for letter in vowels["letter"])
    #count_c = sum(TEXT_lower.count(letter) for letter in consonants["letter"]) 


    vowels = {}
    consonants = {}
    vowels["count"] = count_vowels(TEXT) # Adding key"count" and value "count_vowels(TEXT)" to the dictionary"
    consonants["count"] = count_consonants(TEXT)
    print(f'vowels= {vowels["count"]}')
    print(f'consonants= {consonants["count"]}')

if __name__ == "__main__":
    main()

