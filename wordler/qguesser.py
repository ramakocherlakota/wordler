import QuordlePal
import sys

guesses = []
scores = {}
hard_mode = False
keep_temporary = False
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
            if arg == "--keep-temporary":
                keep_temporary = True
            if arg == "--all":
                scores_table = "all_scores"
            if arg.startswith("--guess"):
                guesses = arg.split("=")[1].split(",")
            if arg.startswith("--score"):
                scoreList = arg.split("=")[1]
                scores[str(i)] = scoreList.split(",")

quordler = QuordlePal.QuordlePal(debug=debug, hard_mode=hard_mode, keep_temporary=keep_temporary)

print(quordler.guess(guesses, scores, 1))


