CREATE TABLE book (
    url TEXT PRIMARY KEY NOT NULL UNIQUE,
    title TEXT,
    image TEXT,
    author TEXT,
    country TEXT,
    language TEXT,
    series TEXT,
    genre TEXT,
    publisher TEXT,
    published TEXT,
    media_type TEXT,
    pages TEXT,
    isbn TEXT,
    oclc TEXT,
    lc_class TEXT,
    dewey_decimal TEXT,
    preceded_by TEXT,
    followed_by TEXT,
    description TEXT,
    other json
);

CREATE TABLE author (
    url TEXT PRIMARY KEY NOT NULL UNIQUE,
    name TEXT,
    image TEXT,
    born TEXT,
    died TEXT,
    education TEXT,
    alma_mater TEXT,
    occupation TEXT,
    period TEXT,
    genre TEXT,
    genres TEXT,
    spouse TEXT,
    children TEXT,
    pen_name TEXT,
    nationality TEXT,
    years_active TEXT,
    subject TEXT,
    notable_works TEXT,
    notable_awards TEXT,
    description TEXT,
    other json
);

CREATE TABLE post (
    url TEXT PRIMARY KEY NOT NULL UNIQUE,
    title TEXT,
    text TEXT
);

CREATE TABLE topic (
    url TEXT PRIMARY KEY NOT NULL UNIQUE,
    title TEXT,
    text TEXT,
    links json
);