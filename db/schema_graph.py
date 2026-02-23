SCHEMA_GRAPH = {
    "student": {
        "description": "Contains academic performance data of students including their marks in various subjects.",
        "use_case": "Use this table when user asks about student marks, scores, performance, grades, subjects like Python, C, Data Structures, Software Engineering, COA.",
        "aliases": [
            "students", "academic", "marks", "grades", "score", "result",
            "pupil", "learner", "candidate", "scholar", "class", "batch",
            "exam", "examination", "test", "assessment", "evaluation",
            "subject", "course", "performance", "report", "report card",
            "scorecard", "transcript", "records", "academic records",
            "university", "college", "school", "education", "studying",
            "semester", "topper", "rank", "ranking", "gpa", "percentage"
        ],
        "columns": {
            "student_name": {
                "type": "VARCHAR",
                "description": "Full name of the student",
                "aliases": [
                    "name", "student", "who", "person", "individual",
                    "candidate name", "full name", "student name",
                    "pupil", "learner", "scholar", "kid", "boy", "girl",
                    "topper", "ranker", "first", "second", "third",
                    "identify", "called", "named"
                ],
                "role": "filter, select"
            },
            "data_structures": {
                "type": "INTEGER",
                "description": "Marks obtained in Data Structures subject out of 100",
                "aliases": [
                    "ds", "data structure", "data structures", "dsa",
                    "data structure and algorithm", "dsa marks",
                    "linked list", "trees", "graphs", "algorithms",
                    "stack", "queue", "array", "heap", "sorting"
                ],
                "role": "aggregation, filter, select"
            },
            "c": {
                "type": "INTEGER",
                "description": "Marks obtained in C programming subject out of 100",
                "aliases": [
                    "c programming", "c language", "c prog",
                    "c subject", "programming in c", "c code",
                    "c marks", "c score", "c lang", "c paper",
                    "pointers", "c syntax", "c exam"
                ],
                "role": "aggregation, filter, select"
            },
            "python": {
                "type": "INTEGER",
                "description": "Marks obtained in Python programming subject out of 100",
                "aliases": [
                    "py", "python programming", "python lang",
                    "python language", "python code", "python marks",
                    "python score", "python subject", "python paper",
                    "python exam", "scripting", "python3", "py3",
                    "django", "flask", "pandas subject", "numpy subject"
                ],
                "role": "aggregation, filter, select"
            },
            "software_engineering": {
                "type": "INTEGER",
                "description": "Marks obtained in Software Engineering subject out of 100",
                "aliases": [
                    "se", "software", "software engineering", "se marks",
                    "se score", "software engg", "software eng",
                    "sdlc", "agile", "waterfall", "software development",
                    "software design", "requirements", "testing subject",
                    "project management subject", "software paper", "se exam",
                    "se subject", "software subject", "system design"
                ],
                "role": "aggregation, filter, select"
            },
            "coa": {
                "type": "INTEGER",
                "description": "Marks obtained in Computer Organization and Architecture subject out of 100",
                "aliases": [
                    "computer organization", "architecture", "computer architecture",
                    "coa marks", "coa score", "coa subject", "coa paper",
                    "coa exam", "computer org", "organization",
                    "processor", "cpu", "memory organization",
                    "instruction set", "isa", "hardware", "assembly",
                    "pipeline", "cache", "registers", "computer hardware subject"
                ],
                "role": "aggregation, filter, select"
            }
        },
        "sample_questions": [
            "Who scored the highest marks in Python?",
            "What is the average marks in Data Structures?",
            "Show top 5 students in C programming",
            "How many students scored more than 80 in COA?",
            "Which student performed best overall?",
            "Who failed in Software Engineering?",
            "List students who got above 90 in Python",
            "What is the lowest score in Data Structures?",
            "Who is the topper in C language?",
            "Show students who scored between 70 and 90 in COA"
        ]
    },

    "cricket": {
        "description": "Contains batting statistics of international cricket players including runs, averages, hundreds, fifties and other performance metrics.",
        "use_case": "Use this table when user asks about cricket players, batting records, runs, averages, centuries, fifties, matches, innings.",
        "aliases": [
            "cricketers", "players", "batsmen", "batting", "cricket stats",
            "cricket", "ipl", "test cricket", "odi", "t20", "international cricket",
            "batter", "batters", "cricket records", "sports", "sport",
            "cricket history", "cricket data", "cricket performance",
            "run scorer", "scorer", "batter stats", "cricket career",
            "world record", "cricket world", "national team", "cricket player",
            "athlete", "sportsman", "legend", "great cricketer", "cricket legend",
            "international player", "cricket database"
        ],
        "columns": {
            "player_name": {
                "type": "VARCHAR",
                "description": "Full name of the cricket player along with their country code",
                "aliases": [
                    "player", "name", "cricketer", "batsman", "who",
                    "athlete", "sportsman", "batter", "person", "individual",
                    "player name", "full name", "international player",
                    "legend", "star", "top player", "best player",
                    "cricket star", "identify", "called", "named",
                    "sachin", "kohli", "dhoni", "rohit", "virat"
                ],
                "role": "filter, select"
            },
            "years_active": {
                "type": "VARCHAR",
                "description": "The years during which the player was active in international cricket",
                "aliases": [
                    "career", "active years", "career span", "years played",
                    "playing years", "career duration", "career length",
                    "active period", "career period", "years in cricket",
                    "career years", "debut", "retirement", "played from",
                    "playing era", "generation", "era", "time period"
                ],
                "role": "filter, select"
            },
            "matches": {
                "type": "VARCHAR",
                "description": "Total number of matches played by the player.",
                "aliases": [
                    "games", "total matches", "matches played", "number of matches",
                    "how many matches", "game count", "appearances",
                    "total games", "matches count", "played", "caps",
                    "international matches", "fixtures", "contests"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "INTEGER"
            },
            "innings": {
                "type": "VARCHAR",
                "description": "Total number of innings played",
                "aliases": [
                    "innings played", "total innings", "number of innings",
                    "how many innings", "batting innings", "times batted",
                    "innings count", "bat", "batting turns", "went in to bat"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "INTEGER"
            },
            "not_outs": {
                "type": "VARCHAR",
                "description": "Number of times the player remained not out",
                "aliases": [
                    "not out", "no", "not outs", "unbeaten", "not dismissed",
                    "times not out", "undefeated innings", "retired not out",
                    "carried bat", "survived innings", "total not outs"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "INTEGER"
            },
            "runs": {
                "type": "VARCHAR",
                "description": "Total runs scored by the player in their career",
                "aliases": [
                    "total runs", "score", "scoring", "run", "runs scored",
                    "career runs", "total score", "aggregate runs",
                    "run tally", "run count", "batting runs", "most runs",
                    "highest runs", "run total", "tally", "accumulated runs",
                    "runs made", "points", "career total"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "INTEGER"
            },
            "high_score": {
                "type": "VARCHAR",
                "description": "Highest score by the player in a single innings.",
                "aliases": [
                    "highest score", "best score", "maximum score", "hs",
                    "top score", "personal best", "pb", "best innings",
                    "highest innings", "max runs", "biggest knock",
                    "career best", "record score", "best knock",
                    "biggest innings", "peak score", "highest knock"
                ],
                "role": "filter, select"
            },
            "batting_average": {
                "type": "VARCHAR",
                "description": "Career batting average of the player",
                "aliases": [
                    "average", "avg", "batting avg", "batting average",
                    "career average", "mean", "per innings average",
                    "run average", "runs per innings", "strike average",
                    "consistency", "average score", "average runs"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "FLOAT"
            },
            "hundreds": {
                "type": "VARCHAR",
                "description": "Total number of centuries (100+ runs) scored by the player",
                "aliases": [
                    "centuries", "100s", "tons", "century", "hundreds scored",
                    "number of centuries", "total centuries", "century count",
                    "how many centuries", "100 plus", "triple figures",
                    "hundred scores", "century tally", "tons scored",
                    "century maker", "centurion", "how many tons"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "INTEGER"
            },
            "fifties": {
                "type": "VARCHAR",
                "description": "Total number of half centuries (50-99 runs) scored by the player",
                "aliases": [
                    "half centuries", "50s", "half tons", "fifties scored",
                    "number of fifties", "total fifties", "fifty count",
                    "how many fifties", "50 plus", "half century",
                    "half centuries scored", "fifty tally", "50s scored",
                    "half tons scored", "50 plus scores"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "INTEGER"
            },
            "ducks": {
                "type": "VARCHAR",
                "description": "Total number of times the player got out for zero runs",
                "aliases": [
                    "zero", "golden duck", "out for zero", "duck count",
                    "how many ducks", "times out for zero", "zero scores",
                    "failures", "dismissed for zero", "scoring zero",
                    "nought", "blob", "total ducks", "duck tally"
                ],
                "role": "aggregation, filter, select",
                "cast_required": True,
                "cast_as": "INTEGER"
            }
        },
        "sample_questions": [
            "Who scored the most runs in cricket?",
            "Which player has the highest batting average?",
            "Show top 10 players by number of centuries",
            "How many matches did Sachin Tendulkar play?",
            "Which player scored the most fifties?",
            "Who has the highest individual score?",
            "Which player has the most ducks?",
            "Show players with more than 10000 career runs",
            "Who has the best batting average among players with 50+ matches?",
            "List players with more than 30 centuries"
        ]
    },

    "employee": {
        "description": "Contains HR and employee data including department, salary, education, experience and performance ratings.",
        "use_case": "Use this table when user asks about employees, salary, department, income, performance, experience, education, gender.",
        "aliases": [
            "employees", "staff", "worker", "hr", "workforce",
            "human resources", "personnel", "team", "people", "member",
            "colleague", "associate", "hire", "hired", "recruit",
            "headcount", "manpower", "labour", "labor", "resource",
            "company", "organization", "office", "workplace",
            "payroll", "compensation", "salary data", "hr data",
            "employee data", "employee records", "staff records",
            "team member", "job", "position", "role", "profile",
            "employee profile", "work", "working", "employed"
        ],
        "columns": {
            "employee_name": {
                "type": "VARCHAR",
                "description": "Full name of the employee",
                "aliases": [
                    "name", "employee", "worker", "staff", "who",
                    "person", "individual", "full name", "employee name",
                    "staff name", "worker name", "colleague", "associate",
                    "team member", "hire", "personnel", "identify",
                    "called", "named", "people", "member name"
                ],
                "role": "filter, select"
            },
            "age": {
                "type": "INTEGER",
                "description": "Age of the employee in years",
                "aliases": [
                    "how old", "years old", "age group", "employee age",
                    "worker age", "old", "young", "senior", "junior",
                    "older", "younger", "age range", "birth year",
                    "oldest", "youngest", "average age", "age bracket"
                ],
                "role": "aggregation, filter, select"
            },
            "department": {
                "type": "VARCHAR",
                "description": "Department where the employee works such as Sales, R&D, Training, Software Development",
                "aliases": [
                    "dept", "team", "division", "sector", "department",
                    "unit", "group", "branch", "section", "area",
                    "function", "domain", "vertical", "business unit",
                    "sales", "r&d", "research", "development", "training",
                    "software development", "engineering", "marketing",
                    "finance", "hr department", "operations", "support",
                    "which department", "what department", "works in",
                    "belongs to", "part of", "assigned to"
                ],
                "role": "filter, select, group by"
            },
            "education": {
                "type": "VARCHAR",
                "description": "Highest education qualification of the employee",
                "aliases": [
                    "qualification", "degree", "educational background",
                    "education level", "highest qualification", "academic background",
                    "academic qualification", "schooling", "study",
                    "masters", "doctorate", "phd", "undergraduate",
                    "bachelors", "btech", "mtech", "mba", "graduate",
                    "postgraduate", "diploma", "certification", "literate",
                    "educated", "learned", "scholar", "studied"
                ],
                "role": "filter, select, group by"
            },
            "gender": {
                "type": "VARCHAR",
                "description": "Gender of the employee - Male or Female",
                "aliases": [
                    "sex", "male", "female", "man", "woman",
                    "men", "women", "boy", "girl", "gender identity",
                    "m", "f", "gender group", "diversity"
                ],
                "role": "filter, select, group by"
            },
            "marital_status": {
                "type": "VARCHAR",
                "description": "Marital status of the employee - Single or Married",
                "aliases": [
                    "married", "single", "relationship status", "marital",
                    "marriage", "wed", "wedded", "spouse", "unmarried",
                    "bachelor", "family status", "civil status",
                    "relationship", "personal status"
                ],
                "role": "filter, select, group by"
            },
            "monthly_income": {
                "type": "INTEGER",
                "description": "Monthly income of the employee in currency units",
                "aliases": [
                    "salary", "income", "pay", "wage", "earnings", "compensation",
                    "monthly salary", "monthly pay", "monthly wage",
                    "monthly earnings", "monthly compensation", "ctc",
                    "cost to company", "package", "remuneration", "stipend",
                    "paycheck", "payslip", "take home", "gross salary",
                    "net salary", "money", "payment", "paid", "earn",
                    "making", "earning", "how much", "income level",
                    "salary range", "highest salary", "lowest salary",
                    "max salary", "min salary", "average salary", "mean salary"
                ],
                "role": "aggregation, filter, select"
            },
            "years_of_experience": {
                "type": "INTEGER",
                "description": "Total years of work experience the employee has",
                "aliases": [
                    "experience", "years", "work experience", "exp",
                    "years of experience", "total experience", "career experience",
                    "professional experience", "job experience", "tenure",
                    "years worked", "working years", "career length",
                    "seniority", "experienced", "fresher", "senior",
                    "junior", "how experienced", "veteran", "industry experience",
                    "years in industry", "work history", "background"
                ],
                "role": "aggregation, filter, select"
            },
            "percent_salary_hike": {
                "type": "INTEGER",
                "description": "Percentage increase in salary given to the employee",
                "aliases": [
                    "hike", "salary hike", "raise", "increment",
                    "pay raise", "pay hike", "salary increment",
                    "salary raise", "appraisal hike", "raise percent",
                    "increase", "salary increase", "pay increase",
                    "how much hike", "hike percentage", "got raise",
                    "increment percentage", "bonus hike", "hike amount",
                    "promotion raise", "annual raise", "yearly hike"
                ],
                "role": "aggregation, filter, select"
            },
            "performance_rating": {
                "type": "INTEGER",
                "description": "Performance rating of the employee on a scale of 1 to 5",
                "aliases": [
                    "rating", "performance", "review", "appraisal",
                    "performance score", "work rating", "job rating",
                    "evaluation", "assessment", "performance review",
                    "work performance", "job performance", "star rating",
                    "score", "ranked", "top performer", "best performer",
                    "high performer", "low performer", "performance level",
                    "kpi", "okr", "performance index", "rated", "how good",
                    "excellent", "outstanding", "average performer",
                    "poor performer", "best rated", "worst rated"
                ],
                "role": "aggregation, filter, select"
            }
        },
        "sample_questions": [
            "Which department has the highest average salary?",
            "Who is the highest paid employee?",
            "How many employees are in the R&D department?",
            "What is the average experience of employees with a Doctorate?",
            "Which employee has the highest performance rating?",
            "Show all female employees in the Sales department",
            "Who got the highest salary hike?",
            "What is the average age of employees in Software Development?",
            "How many married employees are in R&D?",
            "List employees with more than 10 years of experience",
            "Who are the top 5 earners in the company?",
            "Show employees with a Masters degree and salary above 50000",
            "Which department has the most employees?",
            "What is the average salary hike for employees with a Doctorate?"
        ]
    }
}