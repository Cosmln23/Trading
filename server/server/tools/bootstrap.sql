CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS fragments (
  id           VARCHAR(128) PRIMARY KEY,
  doc_id       VARCHAR(128) NOT NULL,
  collection   VARCHAR(64)  NOT NULL,
  page         INTEGER,
  chunk_index  INTEGER,
  text         TEXT         NOT NULL,
  embedding    DOUBLE PRECISION[],
  created_at   TIMESTAMPTZ  DEFAULT now()
);

CREATE TABLE IF NOT EXISTS journal (
  id          SERIAL PRIMARY KEY,
  timestamp   VARCHAR(32)  NOT NULL,
  strategy    VARCHAR(1)   NOT NULL,
  symbol      VARCHAR(32),
  direction   VARCHAR(8),
  entry       DOUBLE PRECISION,
  size        DOUBLE PRECISION,
  stop        DOUBLE PRECISION,
  tp          DOUBLE PRECISION,
  rationale   TEXT,
  tags        TEXT,
  status      VARCHAR(8),
  rr          DOUBLE PRECISION,
  pnl         DOUBLE PRECISION,
  answer_id   VARCHAR(128),
  created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events (
  id          SERIAL PRIMARY KEY,
  time        VARCHAR(16),
  type        VARCHAR(16),
  symbol      VARCHAR(32),
  title       VARCHAR(256),
  created_at  TIMESTAMPTZ DEFAULT now()
);
