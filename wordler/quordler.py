import mysql.connector
from wordler import Wordler

class Quordler(Wordler):
    def __init__(self, guesses, responses, scores_table="scores", debug=False, hard_mode=False):
        self.guesses = guesses
        self.responses = responses
        # 2-D array. [[r11, r12, r13],[r21,r22,r23]..] where rij is the j'th score on the i'th word.
        # So you can take the guesses together with [ri1, ri2, ri3..] as representing an individual wordle

        self.guess_count = len(self.guesses) # len([s11, s12, ... ])
        self.word_count = len(self.responses) # number of words we're shooting for.  4 in classic quordle, 1 in wordle
        
        self.scores_table = scores_table
        self.hard_mode = hard_mode 
        self.debug = debug
        self.dbh = None
            
    def add_guess(self, guess, scores):
        self.guesses.append(guess)
        for j in range(self.word_count):
            self.responses[j].append[scores[j]]

    def get_score(self, targets, guess):
        froms = []
        wheres = []
        projections = []
        i = 0
        for target in targets:
            froms.append(f"{self.scores_table} as a_{i}")
            wheres.append(f"a_{i}.guess = '{guess}' and a_{i}.answer = '{target}'")
            projections.append(f"a_{i}.score as score_{i}")
            i = i + 1
        from_clause = ", ".join(froms)
        where_clause = " and ".join(wheres)
        projection_clause = ", ".join(projections)
        cursor = self.query(f"select {projection_clause} from {from_clause} where {where_clause}")
        for (scores) in cursor:
            return (scores)

    def unique_solution(self):
        subqueries = []
        subquery = ""
        i = 0
        for guess_score in self.guess_scores:
            (guess, score) = guess_score
            if i > 0:
                subqueries.append(f"answer in (select answer from {self.scores_table} where guess='{guess}' and score='{score}')")            
            else:
                subqueries.append(f"guess='{guess}' and score='{score}'")            
            i = i + 1
        subquery =   " and ".join(subqueries)
        sql = f"select count(*) as c, min(answer) from {self.scores_table} where {subquery} "
        csr = self.query(sql)
        for (c, answer) in csr:
            if c == 1:
                return (answer, None)
            else:
                return False

    def conditional_entropy(self, guess, score):
        sql = f"select log(count(*))/log(2) as h, 0 from {self.scores_table} where guess='{guess}' and score='{score}' "
        csr = self.query(sql)
        for (h, ignore) in csr:
            return h

    def guess_projections(self):
#           guess
#           , sum(c_1 * log(c_1) / log(2)) / sum(c_1) as h_1
#           , sum(c_2 * log(c_2) / log(2)) / sum(c_2) as h_2
#           , sum(c_3 * log(c_3) / log(2)) / sum(c_3) as h_3
#           , sum(c_1 * log(c_1) / log(2)) / sum(c_1) + sum(c_2 * log(c_2) / log(2)) / sum(c_2) + sum(c_3 * log(c_3) / log(2)) / sum(c_3) as h_total
        terms = []
        for j in range(self.word_count) :
            terms.append(f"sum(c_{j} * log(c_{j}) / log(2)) / sum(c_{j})")
        return "guess, " + ", ".join(terms) + ", " + " + ".join(terms)

          
    def guess_subselects_projections(self):
        projs = ["g.guess"]
        for j in range(self.word_count):
            projs.append(f"a_{j}.score, a_{j}.count(*) as c_{j}")
        return ", ".join(projs)

    def guess_subselects_from_clause(self):
        froms = ["guesses g"]
        for j in range(self.word_count):
            projs.append(f"scores as a_{j}")
        return ", ".join(froms)

# select guess, sum(c * log(c) / log(2)) / sum(c) as h from (select g.guess, score, count(*) as c from scores a, guesses g where a.guess = g.guess  and answer in (select answer from scores where guess='raise' and score='-W---')  group by 1, 2) as t1  group by 1 order by 2, 1 limit 1

    def guess_subselects_where_clause(self):
        wheres = []
        for j in range(self.word_count):
            wheres.append(f"g.guess = a_{j}.guess and {self.guess_subsubselect(j)}")
        return " and ".join(wheres)

#    def guess_subsubselect(self, j):
        

#    def guess_subselects(self):
        # something like  
        # select g.guess, a_1.score, a1.count(*) as c_1 from guesses g, scores a_1 where a_1.guess = g.guess and a1.answer in (sub_subselect_1_1) and a1.answer in (sub_subselect_1_2) and...
        

#    def guess_sub_subselect(self, guess_i, score_i_j):
        # something like
        # (select answer from scores where guess={guess_1} ans score={score_1_1})) 

    def next_guess(self):
        query = f"select {guess_projections()} from {guess_subselects()} where {guess_where_clauses()}"
        subqueries = []
        subquery = ""
        hard_mode_subqueries = []
        hard_mode_subquery = ""
        for guess_scores in self.guess_scores:
            (guess, scores) = guess_scores
            subqueries.append(f"answer in (select answer from {self.scores_table} where guess='{guess}' and score='{score}')")            
        subquery =  " and " + " and ".join(subqueries)
#         csr = self.query(query)
#         retval = None
#         for (guess, entropy) in csr:
#             retval = (guess, entropy)
#         return retval

    def get_random_answer(self):
        csr = self.query("select answer, 0 from answers order by rand() limit 1")
        for (answer, ignore) in csr:
            return answer

    def solve(self, target, guess):
        score = self.get_score(target, guess)
        entropy = self.conditional_entropy(guess, score)
        retval = [[guess, score, entropy]]
        self.add_guess(guess, score)
        while True:
            (guess, entropy) = self.next_guess()
            score = self.get_score(target, guess)
            if score == "BBBBB":
                retval.append([guess, score, 0.00])
                break
            if entropy:
                retval.append([guess, score, entropy])
                self.add_guess(guess, score)
            else:
                retval.append([guess, score])
                if target != guess:
                    retval.append([target, "BBBBB", 0.00])
                break
        return retval
