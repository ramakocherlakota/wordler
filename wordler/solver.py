import sys
import wordler

target = None
hard_mode = False
debug = False
scores_table = "scores"
guess = "raise"

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
                guess = "soare"
        else:
            target = arg

if not target:
    print("You must provide a target word")
    exit(1)

wordler = wordler.Wordler(debug=debug, scores_table=scores_table, hard_mode=hard_mode)

if not wordler.get_score(target, target):
    print(target + " is not a valid answer")
    exit(1)

score = wordler.get_score(target, guess)
entropy = wordler.conditional_entropy(guess, score)
i = 1
print(f"{i}. {guess} -> {score} [{entropy}]" )

wordler.add_guess(guess, score)

while True:
    i = i + 1
    (guess, entropy) = wordler.next_guess()
    score = wordler.get_score(target, guess)
    if entropy:
        print(f"{i}. {guess} -> {score} [{entropy}]")
        wordler.add_guess(guess, score)
    else:
        print(f"{i}. {guess} -> {score} ")
        if target != guess:
            print(f"{i+1}. {target} -> BBBBB ")
        break






