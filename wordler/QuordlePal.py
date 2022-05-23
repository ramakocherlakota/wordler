import mysql.connector

class QuordlePal:

    def __init__(self, scores_table="scores", starting_word="raise", debug=False, hard_mode=False, host="127.0.0.1", username="wordle", password="", database="wordle", keep_temporary=False):
        self.scores_table = scores_table
        self.hard_mode = hard_mode 
        self.starting_word = starting_word 
        self.debug = debug
        self.dbh = None
        self.username = username
        self.password = password
        self.database = database
        self.host = host
        if keep_temporary:
            self.temporary = ""
        else:
            self.temporary = "temporary"

    def db(self):
        if self.dbh is None:
            self.dbh = mysql.connector.connect(user=self.username, password=self.password,
                                               host=self.host,
                                               database=self.database)
        return self.dbh

    def query(self, sql, title=None):
        cursor = self.db().cursor()
        if self.debug and title is not None:
                print(f">> {title}: {sql}")
        cursor.execute(sql)
        return cursor
    
    def guess_table(self, name, guesses, responses):
        wheres = ["a.guess = g.guess"]
        for i in range(len(guesses)):
            wheres.append(f"answer in (select answer from {self.scores_table} where guess = '{guesses[i]}' and score = '{responses[i]}')")
            wheres.append(f"g.guess != '{guesses[i]}'")

        where_clause = "where " + " and ".join(wheres)
        sql = f"select g.guess, score, g.guess in (select answer from {self.scores_table} where '{guesses[i]}'= guess and '{responses[i]}' = score) as hard, count(*) as c from {self.scores_table} a, guesses g {where_clause} group by 1, 2, 3"
        self.query(f"drop {self.temporary} table if exists {name}")
        self.query(f"create {self.temporary} table {name} as {sql}", "creating temp table")
        self.query(f"alter table {name} add primary key(guess, score), add key(score, guess)")

    def get_score(self, target, guess):
        cursor = self.query(f"select score, 0 from {self.scores_table} where guess='{guess}' and answer='{target}'", "computing score")
        for (score, ignore) in cursor:
            return score

    def get_random_answer(self):
        csr = self.query("select answer, 0 from (select distinct(answer) from scores) as c order by rand() limit 1")
        for (answer, ignore) in csr:
            return answer

    def guessable_solution(self, guesses, responses):
        subqueries = []
        subquery = ""
        if len(guesses) == 0:
            return False
        for i in range(len(guesses)):
            guess = guesses[i]
            score = responses[i]
            if i > 0:
                subqueries.append(f"answer in (select answer from {self.scores_table} where guess='{guess}' and score='{score}')")            
            else:
                subqueries.append(f"guess='{guess}' and score='{score}'")            
            subquery =   " and ".join(subqueries)
        sql = f"select count(*) as c, min(answer) from {self.scores_table} where {subquery} "
        csr = self.query(sql,  "guessable")
        for (c, answer) in csr:
            return (c, answer)

    def guess(self, guesses, scores) :
        for target in scores:
            (count, answer) = self.guessable_solution(guesses, scores[target])
            if count == 1:
                return [answer, None]
        
        tables = []

        for target in scores:
            target_scores = scores[target]
            self.guess_table(f"q_{target}", guesses, target_scores)
            self.collate_table(f"q_{target}", f"r_{target}")
            tables.append(f"r_{target}")

        return self.min_sum_entropy(tables)

    def collate_table(self, source, dest) :
        self.query(f"drop {self.temporary} table if exists {dest}")
        hard_clause = ""
        if self.hard_mode :
            hard_clause = " and hard "
        self.query(f"create {self.temporary} table {dest} as select g.guess, sum({source}.c * log({source}.c) / log(2)) / sum({source}.c) as h from guesses g, {source} where {source}.guess = g.guess {hard_clause} group by 1", "collating response")
        self.query(f"alter table {dest} add key(guess)")

    def min_sum_entropy(self, tables) :
        sums = []
        wheres = []
        hards = []
        for table in tables:
            sums.append(f"{table}.h")
            wheres.append(f"{table}.guess = g.guess")
            hards.append(f"{table}.hard")
        sums_clause = " + ".join(sums)
        tables_clause = ", ".join(tables)
        where_clause = " and ".join(wheres)
        sql = f"select g.guess, {sums_clause} from guesses g, {tables_clause} where {where_clause} order by 2 limit 1"
        csr = self.query(sql, "min sum entropy")
        for (guess, entropy) in csr:
            return (guess, entropy)

    def conditional_entropy(self, guess, score):
        sql = f"select log(count(*))/log(2) as h, 0 from {self.scores_table} where guess='{guess}' and score='{score}' "
        csr = self.query(sql, "conditional entropy")
        for (h, ignore) in csr:
            return h

    def solve(self, targets, max_iterations=20):
        guess = self.starting_word
        found = {}
        guesses = [guess]

        scores = {}
        entropy = 0
        for target in targets:
            score = self.get_score(target, guess)
            entropy = entropy + self.conditional_entropy(guess, score)
            scores[target] = [score]
        entropies = [entropy]

        iteration = 1
        while len(scores) > 0 and iteration != max_iterations:
            (guess, entropy) = self.guess(guesses, scores)
            guesses.append(guess)
            entropies.append(entropy)

            pop_me = []
            for target in scores:
                score = self.get_score(target, guess)
                scores[target].append(score)
                if score == 'BBBBB':
                    pop_me.append(target)

            for target in pop_me:
                found[target] = len(scores.pop(target))
            
            iteration = iteration + 1

        return {"guesses":guesses, "scores":found}
            
