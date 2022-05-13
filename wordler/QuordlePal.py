from WordlePal import WordlePal

class QuordlePal(WordlePal):
    
    def guess(self, guesses, responses) :
        for i in range(len(responses)) :
            (count, answer) = self.guessable_solution(guesses, responses[i])
            if count == 1:
                return [answer, None]
        
        tables = []
        for i in range(len(responses)) :
            tables.append(f"q_{i}")
            self.guess_table(f"q_{i}", guesses, responses[i])
        return self.min_sum_entropy(tables)

    def min_sum_entropy(self, tables) :
        sums = []
        wheres = []
        hards = []
        for table in tables:
            sums.append(f"sum({table}.c * log({table}.c) / log(2)) / sum({table}.c)")
            wheres.append(f"{table}.guess = g.guess")
            hards.append(f"{table}.hard")
        hard_mode_clause = ""
        if self.hard_mode:
            hard_mode_clause = " and (" + " or ".join(hards)
        sums_clause = " + ".join(sums)
        tables_clause = ", ".join(tables)
        where_clause = " and ".join(wheres) + hard_mode_clause
        sql = f"select g.guess, {sums_clause} from guesses g, {tables_clause} where {where_clause} group by 1 order by 2, 1 limit 1"
        csr = self.query(sql, "min sum entropy")
        for (guess, entropy) in csr:
            return (guess, entropy)

    def get_multi_score(self, targets, guess):
        scores = []
        for target in targets:
            score = self.get_score(target, guess)
            scores.append(score)
        return scores

    def get_min_coditional_entropy(self, scores, guess):
        entropies = []
        for target in targets:
            entropy = self.conditional_entropy(score, guess)
            entropies.append(entropy)
        return min(entropies)
    
    def solve(self, targets, max_iterations=20):
        guess = self.starting_word

        found = {}

        guesses = [guess]
        scores = [self.get_multi_scores(targets, guess)]
        entropies = [get_min_coditional_entropy(scores, guess)]

        iteration = 1
        while iteration != max_iterations:
            (guess, entropy) = self.guess(guesses, scores)
            guesses.append(guess)
            entropies.append(entropy)
            scores.append(self.get_multi_score(targets, guess))

            for j in range(len(scores)):
                if scores[j] == 'BBBBB':
                    target = targets[j]
                    found[target] = iteration
                    targets.remove(target)

            iteration = iteration + 1

        print(guesses)
        print(found)
            
