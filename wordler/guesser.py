import sys
import wordler

guess_scores = []
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        guess_score = arg.split("=")
        guess_scores.append(guess_score)

wordler = wordler.Wordler(guess_scores=guess_scores, debug=True)

print (wordler.next_guess())


