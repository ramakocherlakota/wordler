import sys

def count_in(c, w):
    num = 0
    for let in w:
        if let == c:
            num = num + 1
    return num

def score(answer, guess) :
    score = []
    answer_counts = {}
    min_counts = {}
    for c in answer:
        answer_counts[c] = count_in(c, answer)

    for c in guess:
        if c in answer_counts:
            gc = count_in(c, guess)
            min_counts[c] =  gc if gc < answer_counts[c] else answer_counts[c]

    for i in range(len(answer)):
        g = guess[i]
        if g == answer[i] :
            score.append("B")
            min_counts[g] = min_counts[g] - 1
        else:
            score.append(" ")

    for i in range(len(answer)):
        g = guess[i]
        if score[i] == " ":
            if g in min_counts and  min_counts[g] > 0:
                score[i] = "W"
                min_counts[g] = min_counts[g] - 1
    
    return "".join(score)
    
def read_words(filename):
    words = []
    with open(filename) as f:
        unstripped = f.readlines()
    for w in unstripped:
        words.append(w.strip())
    return words

answers = read_words(sys.argv[1])
words = read_words(sys.argv[2])

for answer in answers:
    for guess in words:
        sc = score(answer, guess)
        print(f"{answer}|{guess}|{sc}")
