import sys
import WordlePal

wordlePal = WordlePal.WordlePal(debug=False, hard_mode=True)
print(wordlePal.guess(["raise", "cloth", "opine"], ["--b-b", "--w--", "b-bbb"]))
#print(wordlePal.guess(["raise", "cloth"], ["--b-b", "--w--"]))
#print(wordlePal.guess(["raise", "cloth"], ["--b-b", "-bw--"]))
