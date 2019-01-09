
CREATE TABLE types (

  id         SERIAL PRIMARY KEY,
  type       VARCHAR(200) UNIQUE

);


CREATE TABLE stat_origin (

  id         SERIAL PRIMARY KEY,
  origin     VARCHAR(200) UNIQUE

);

CREATE TABLE stat_source (

  id         SERIAL PRIMARY KEY,
  source     VARCHAR(200) UNIQUE

);

CREATE TABLE stat_context (

  id         SERIAL PRIMARY KEY,
  context    VARCHAR(200) UNIQUE

);


CREATE TABLE stat (

  id         SERIAL PRIMARY KEY,
  origin_id  INT REFERENCES stat_origin(id), 
  source_id  INT REFERENCES stat_source(id),
  context_id INT REFERENCES stat_context(id),
  type_id    INT REFERENCES types(id),  

  log        VARCHAR(200),
  ts         timestamp DEFAULT now()

);


CREATE TABLE event_origin (

  id         SERIAL PRIMARY KEY,
  origin     VARCHAR(200) UNIQUE

);

CREATE TABLE event_source (

  id         SERIAL PRIMARY KEY,
  source     VARCHAR(200) UNIQUE

);


CREATE TABLE event_context (

  id         SERIAL PRIMARY KEY,
  context    VARCHAR(200) UNIQUE

);



CREATE TABLE event (

  id         SERIAL PRIMARY KEY,
  origin_id  INT REFERENCES event_origin(id),
  source_id  INT REFERENCES event_source(id),
  context_id INT REFERENCES event_context(id),
  type_id    INT REFERENCES types(id),  

  log        VARCHAR(200),
  ts         timestamp DEFAULT now()

);
