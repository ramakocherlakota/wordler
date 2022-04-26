import sys
import WordlePal

wordlePal = WordlePal.WordlePal(debug=True, hard_mode=False)
#print(wordlePal.solve(sys.argv[1]))
wordlePal.guess_table("t2", ["raise", "empty", "chalk", "aback"], ['WB--W', 'W--W-', '--W--', 'W----'], temporary="")
##wordlePal.guess_table("t1", ["raise"], ['WB--W'], temporary="")
