--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: matches; Type: TABLE; Schema: public; Owner: laurenortencio; Tablespace: 
--

CREATE TABLE matches (
    match_id integer NOT NULL,
    tournament_id integer,
    round_num integer,
    player_1 character varying(20),
    player_2 character varying(20)
);


ALTER TABLE matches OWNER TO laurenortencio;

--
-- Name: matches_match_id_seq; Type: SEQUENCE; Schema: public; Owner: laurenortencio
--

CREATE SEQUENCE matches_match_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE matches_match_id_seq OWNER TO laurenortencio;

--
-- Name: matches_match_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: laurenortencio
--

ALTER SEQUENCE matches_match_id_seq OWNED BY matches.match_id;


--
-- Name: positions; Type: TABLE; Schema: public; Owner: laurenortencio; Tablespace: 
--

CREATE TABLE positions (
    tournament_id integer NOT NULL,
    table_id character varying(10) NOT NULL,
    "left" character varying(20),
    top character varying(20)
);


ALTER TABLE positions OWNER TO laurenortencio;

--
-- Name: tournaments; Type: TABLE; Schema: public; Owner: laurenortencio; Tablespace: 
--

CREATE TABLE tournaments (
    tournament_id integer NOT NULL,
    tournament_name character varying(50) NOT NULL,
    url character varying(50) NOT NULL,
    stream character varying(50) NOT NULL,
    max_stations integer,
    user_id integer
);


ALTER TABLE tournaments OWNER TO laurenortencio;

--
-- Name: tournaments_tournament_id_seq; Type: SEQUENCE; Schema: public; Owner: laurenortencio
--

CREATE SEQUENCE tournaments_tournament_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tournaments_tournament_id_seq OWNER TO laurenortencio;

--
-- Name: tournaments_tournament_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: laurenortencio
--

ALTER SEQUENCE tournaments_tournament_id_seq OWNED BY tournaments.tournament_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: laurenortencio; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(20) NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    user_type character varying(11) NOT NULL,
    phone character varying(11)
);


ALTER TABLE users OWNER TO laurenortencio;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: laurenortencio
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO laurenortencio;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: laurenortencio
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: match_id; Type: DEFAULT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY matches ALTER COLUMN match_id SET DEFAULT nextval('matches_match_id_seq'::regclass);


--
-- Name: tournament_id; Type: DEFAULT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY tournaments ALTER COLUMN tournament_id SET DEFAULT nextval('tournaments_tournament_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: matches; Type: TABLE DATA; Schema: public; Owner: laurenortencio
--

COPY matches (match_id, tournament_id, round_num, player_1, player_2) FROM stdin;
\.


--
-- Name: matches_match_id_seq; Type: SEQUENCE SET; Schema: public; Owner: laurenortencio
--

SELECT pg_catalog.setval('matches_match_id_seq', 1, false);


--
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: laurenortencio
--

COPY positions (tournament_id, table_id, "left", top) FROM stdin;
1	table5	495	227
1	table1	72	50
1	table3	495	50
1	table2	294	10
2	table1	72	50
2	table2	309	50
2	table4	309	227
2	table3	524	21
2	table5	538	250
1	table4	309	227
\.


--
-- Data for Name: tournaments; Type: TABLE DATA; Schema: public; Owner: laurenortencio
--

COPY tournaments (tournament_id, tournament_name, url, stream, max_stations, user_id) FROM stdin;
1	Turni 2015	turni2015	twitch.tv/ZeRo	16	1
2	Turni International 2015	turni2015	twitch.tv/nakat973	16	1
\.


--
-- Name: tournaments_tournament_id_seq; Type: SEQUENCE SET; Schema: public; Owner: laurenortencio
--

SELECT pg_catalog.setval('tournaments_tournament_id_seq', 2, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: laurenortencio
--

COPY users (user_id, username, email, password, user_type, phone) FROM stdin;
1	lencat	laurenortencio@gmail.com	1	Organizer	6263846432
2	meowchi	meowchi@gmail.com	1	Organizer	1
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: laurenortencio
--

SELECT pg_catalog.setval('users_user_id_seq', 2, true);


--
-- Name: matches_pkey; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_pkey PRIMARY KEY (match_id);


--
-- Name: positions_pkey; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (tournament_id, table_id);


--
-- Name: tournaments_pkey; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_pkey PRIMARY KEY (tournament_id);


--
-- Name: tournaments_tournament_name_key; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_tournament_name_key UNIQUE (tournament_name);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: matches_tournament_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY matches
    ADD CONSTRAINT matches_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id);


--
-- Name: positions_tournament_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY positions
    ADD CONSTRAINT positions_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id);


--
-- Name: tournaments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: laurenortencio
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM laurenortencio;
GRANT ALL ON SCHEMA public TO laurenortencio;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

