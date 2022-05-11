import sys
import WordlePal

wordlePal = WordlePal.WordlePal(debug=True, hard_mode=False, keep_temporary=True)

#print(wordlePal.solve(sys.argv[1]))


print(wordlePal.guess(["raise"], ['-----']))


##wordlePal.guess_table("t1", ["raise"], ['WB--W'], temporary="")
