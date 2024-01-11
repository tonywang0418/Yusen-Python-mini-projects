#!/usr/bin/python3
# This script will count the number of vowels and consonants in a text.
# YW-20240109

TEXT = "Yes and No are not the only answers. In the intricate and sometimes perplexing realm of security, the straightforward ‘yes’ and ‘no’ answers we’re accustomed to may suddenly seem elusive. It’s a humorous take on the intricacies of security, where the right answer might be 'Well, it depends,' and navigating the security landscape feels a bit like solving a riddle. Welcome to the world where black and white answers are a rare find and shades of gray are supreme. The majority of security breaches are caused by human error. Even though you send out reminder emails and try to teach everyone the cybersecurity safety practices, because humans are evolved to trust people, someone will always trust the wrong person causing a breach. It’s like trying to teach a goldfish to play fetch. So, while you keep fighting the good fight against digital chaos, you secretly wish that human error would take a vacation. Todays tip: MFA enabled? Make sure you have it enabled and not someone else!! In a world where cyberattacks are the uninvited party crashers, MFA is the door policy we can all get behind even if it does involve a lot of training and begging to get people to use it. Clicking on a phishing link is like taking a stroll through a cyberjungle and stumbling upon a sign that says, “Free treasure ahead!” It’s as if your computer suddenly transformed into an adventurous pirate ship, setting sail on the high seas of the internet. But here’s the catch: instead of buried treasure, you find yourself face-to-face with malware that’s more mischievous than a band of pirate monkeys raiding your digital coconuts."  
text_low = TEXT.lower()
vowels = "aeiou" 
vowels_count = {}
consonants_count = {}

for char in text_low: #use for loop to count each letter and save it to the dictionary" 
    if char.isalpha():
        if char in vowels:
            vowels_count[char] = vowels_count.get(char, 0) + 1 #assign value to the key. if there is value then +1, if no value yet, it starts from 0 and +1
        else:
            consonants_count[char] = consonants_count.get(char, 0) + 1
    

def sum_calculate(dictionary):
    """sum calculation when I put dictionary in ()"""
    return sum(dictionary.values())

def main():
    """print sum and dictionaries out"""
    print(f'vowels= {sum_calculate(vowels_count)}')
    print(f'consonants= {sum_calculate(consonants_count)}')
    print(f'vowels= {vowels_count}')
    print(f'consonants= {consonants_count}')
if __name__ == "__main__":
    main()

