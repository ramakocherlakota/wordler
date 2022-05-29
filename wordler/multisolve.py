import fileinput, sys
import QuordlePal

hard_mode = False
keep_temporary = False
debug = False
scores_table = "scores"
starting_word = "raise"

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg.startswith("-"):
            if arg == "--hard":
                hard_mode = True
            if arg == "--debug":
                debug = True
            if arg == "--keep-temporary":
                keep_temporary = True
            if arg == "--all":
                scores_table = "all_scores"

quordler = QuordlePal.QuordlePal(debug=debug, scores_table=scores_table, starting_word=starting_word, hard_mode=hard_mode, keep_temporary=keep_temporary)

for line in fileinput.input():
    word = line.rstrip()
    solution = quordler.solve([word])
    sys.stderr.write(f"{word}|{solution['attempts']}|{solution['guesses']}\n")
    print(f"{word}|{solution['attempts']}|{solution['guesses']}|{solution}")
