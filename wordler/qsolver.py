import QuordlePal
import sys

targets = []
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
        else:
            targets.append(arg)

if len(targets) == 0:
    print("You must provide target word(s)")
    exit(1)

quordler = QuordlePal.QuordlePal(debug=debug, scores_table=scores_table, starting_word=starting_word, hard_mode=hard_mode, keep_temporary=keep_temporary)

for target in targets:
    if not quordler.get_score(target, target):
        print(target + " is not a valid answer")
        exit(1)

solution = quordler.solve(targets)
print(solution)
