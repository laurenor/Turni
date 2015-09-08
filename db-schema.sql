--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.4
-- Dumped by pg_dump version 9.4.4
-- Started on 2015-09-07 21:02:11 PDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 177 (class 3079 OID 12123)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2285 (class 0 OID 0)
-- Dependencies: 177
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 176 (class 1259 OID 26031)
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
-- TOC entry 175 (class 1259 OID 26018)
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
-- TOC entry 174 (class 1259 OID 26016)
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
-- TOC entry 2286 (class 0 OID 0)
-- Dependencies: 174
-- Name: tournaments_tournament_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: laurenortencio
--

ALTER SEQUENCE tournaments_tournament_id_seq OWNED BY tournaments.tournament_id;


--
-- TOC entry 173 (class 1259 OID 26010)
-- Name: users; Type: TABLE; Schema: public; Owner: laurenortencio; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(20) NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    phone character varying(11)
);


ALTER TABLE users OWNER TO laurenortencio;

--
-- TOC entry 172 (class 1259 OID 26008)
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
-- TOC entry 2287 (class 0 OID 0)
-- Dependencies: 172
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: laurenortencio
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- TOC entry 2158 (class 2604 OID 26021)
-- Name: tournament_id; Type: DEFAULT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY tournaments ALTER COLUMN tournament_id SET DEFAULT nextval('tournaments_tournament_id_seq'::regclass);


--
-- TOC entry 2157 (class 2604 OID 26013)
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- TOC entry 2166 (class 2606 OID 26035)
-- Name: positions_pkey; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (tournament_id, table_id);


--
-- TOC entry 2162 (class 2606 OID 26023)
-- Name: tournaments_pkey; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_pkey PRIMARY KEY (tournament_id);


--
-- TOC entry 2164 (class 2606 OID 26025)
-- Name: tournaments_tournament_name_key; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_tournament_name_key UNIQUE (tournament_name);


--
-- TOC entry 2160 (class 2606 OID 26015)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: laurenortencio; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 2168 (class 2606 OID 26036)
-- Name: positions_tournament_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY positions
    ADD CONSTRAINT positions_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id);


--
-- TOC entry 2167 (class 2606 OID 26026)
-- Name: tournaments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: laurenortencio
--

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- TOC entry 2284 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: laurenortencio
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM laurenortencio;
GRANT ALL ON SCHEMA public TO laurenortencio;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-09-07 21:02:11 PDT

--
-- PostgreSQL database dump complete
--

