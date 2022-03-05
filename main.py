from tokenizer import tokenize
test = """DECLARE ScoreOne : INTEGER
DECLARE ScoreTwo : INTEGER
DECLARE HighestScore : INTEGER

ScoreOne << INPUT
ScoreTwo << INPUT
HighestScore << 54000

IF ScoreOne > ScoreTwo THEN 
    OUTPUT "PlayerOne beat PlayerTwo!"
    IF ScoreOne > HighestScore THEN
        OUTPUT ScoreOne, " is the new high score!"
    ENDIF
ELSE
    OUTPUT "PlayerOne lost!"
ENDIF"""

tokens = tokenize(test)
print(tokens)