import fileinput, sys
import QuordlePal

hard_mode = True
keep_temporary = False
debug = False
scores_table = "scores"
starting_word = "raise"

quordler = QuordlePal.QuordlePal(debug=debug, scores_table=scores_table, starting_word=starting_word, hard_mode=hard_mode, keep_temporary=keep_temporary)

for line in fileinput.input():
    word = line.rstrip()
    solution = quordler.solve([word])
    sys.stderr.write(f"{word}|{solution['attempts']}|{solution['guesses']}\n")
    print(f"{word}|{solution['attempts']}|{solution['guesses']}|{solution}")
