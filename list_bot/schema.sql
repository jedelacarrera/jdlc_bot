CREATE TABLE lists (
    id SERIAL PRIMARY KEY,
    name TEXT,
    conversation TEXT NOT NULL
);

CREATE TABLE participants (
	id SERIAL PRIMARY KEY,
	list_id INTEGER REFERENCES lists(id),
	phone TEXT,
	name TEXT,
	comment TEXT,
	going BOOLEAN
);

