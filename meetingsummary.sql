CREATE TABLE meeting (
    ID TEXT PRIMARY KEY,
    Title Text,
    MeetingDate Text,
    Attendees Text,
    Agenda Text,
    ActionItems Text,
    Notes Text,
    Transcript Text,
    Recording Text
);

CREATE TABLE line (
    ID TEXT PRIMARY KEY,
    Meeting Text,
    TStamp TEXT,
    Speaker TEXT,
    Verbatim TEXT,
    SENT_POS REAL,
    SENT_NEU REAL,
    SENT_NEG REAL,
    Sentiment REAL,
    FOREIGN KEY(Meeting) REFERENCES meeting(ID)
);

CREATE TABLE summary (
    Speaker TEXT PRIMARY KEY,
    Meeting Text,
    ShortSummary TEXT,
    LongSummary TEXT,
    Allsaid TEXT,
    FOREIGN KEY(Meeting) REFERENCES meeting(ID)
);

CREATE TABLE entity (
    Entity TEXT PRIMARY KEY,
    Variants TEXT
);

CREATE TABLE ranks (
    Entity TEXT PRIMARY KEY,
    Score Integer
);

CREATE TABLE occurance (
    ID TEXT Primary KEY,
    Entity TEXT,
    Line_ID TEXT
);

CREATE VIEW speaker_list AS 
    SELECT DISTINCT Speaker
    FROM line;

CREATE VIEW verbatims AS
    SELECT Speaker, Verbatim 
    FROM line;

CREATE VIEW KWIC AS
    SELECT occurance.Entity, 
    line.TStamp, 
    line.Speaker, 
    line.Verbatim, 
    line.Sentiment 
    FROM occurance 
    INNER JOIN line ON line.ID=occurance.Line_ID;