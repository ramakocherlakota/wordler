import sys
import WordlePal

guesses = []
scores = []
hard_mode = False
debug = False
scores_table = "scores"
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg.startswith("-"):
            if arg == "--hard":
                hard_mode = True
            if arg == "--debug":
                debug = True
            if arg == "--all":
                scores_table = "all_scores"
        else:
            guess_score = arg.split("=")
            guesses.append(guess_score[0])
            scores.append(guess_score[1])

wordler = WordlePal.WordlePal(debug=debug, hard_mode=hard_mode)

print(wordler.guess(guesses, scores))


