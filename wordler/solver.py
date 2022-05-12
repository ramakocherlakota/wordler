import sys
import WordlePal

target = None
hard_mode = False
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
            if arg == "--all":
                scores_table = "all_scores"
                starting_word = "soare"
            if arg == "--random":
                target = "--random"
        else:
            target = arg

if not target:
    print("You must provide a target word")
    exit(1)

wordler = WordlePal.WordlePal(debug=debug, scores_table=scores_table, starting_word=starting_word, hard_mode=hard_mode)

if target == "--random":
    target = wordler.get_random_answer()
    print(f"wordling for random word {target}")

if not wordler.get_score(target, target):
    print(target + " is not a valid answer")
    exit(1)

solution = wordler.solve(target)
print(solution)
