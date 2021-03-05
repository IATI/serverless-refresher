upgrade = """
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE TYPE public.att_data_type AS ENUM (
    'date',
    'string',
    'numeric',
    'boolean'
);

SET default_tablespace = '';

CREATE TABLE public.attribute (
    md5_pk uuid NOT NULL,
    name character varying NOT NULL,
    date_value timestamp without time zone,
    string_value character varying,
    numeric_value numeric,
    boolean_value boolean
);

CREATE TABLE public.attribute_type (
    name character varying NOT NULL,
    type public.att_data_type
);

CREATE TABLE public.element (
    md5_pk uuid NOT NULL,
    name character varying NOT NULL,
    text_raw text,
    text_tokens tsvector,
    is_root boolean NOT NULL
);

CREATE TABLE public.element_to_activity (
    element_key uuid NOT NULL,
    activity_key uuid NOT NULL
);

CREATE TABLE public.element_to_attribute (
    element_key uuid NOT NULL,
    attribute_key uuid NOT NULL
);

CREATE TABLE public.element_to_child (
    element_key uuid NOT NULL,
    child_key uuid NOT NULL
);

CREATE TABLE public.element_to_parent (
    element_key uuid NOT NULL,
    parent_key uuid NOT NULL
);

CREATE TABLE public.refresher (
    id character varying NOT NULL,
    hash character varying NOT NULL,
    url character varying NOT NULL,
    first_seen timestamp without time zone NOT NULL,
    last_seen timestamp without time zone NOT NULL,
    modified timestamp without time zone,
    downloaded timestamp without time zone,
    download_error integer,
    validation_request timestamp,
    validation_api_error integer,
    valid boolean,
    datastore_processing_start timestamp without time zone,
    datastore_processing_end timestamp without time zone,
    datastore_root_element_key uuid
);

CREATE TABLE public.version (
    number character varying NOT NULL,
    migration integer NOT NULL
);

INSERT INTO public.attribute_type VALUES ('version', 'string');
INSERT INTO public.attribute_type VALUES ('generated-datetime', 'date');
INSERT INTO public.attribute_type VALUES ('linked-data-default', 'string');
INSERT INTO public.attribute_type VALUES ('type', 'string');
INSERT INTO public.attribute_type VALUES ('default-currency', 'string');
INSERT INTO public.attribute_type VALUES ('linked-data-uri', 'string');
INSERT INTO public.attribute_type VALUES ('budget-not-provided', 'string');
INSERT INTO public.attribute_type VALUES ('role', 'string');
INSERT INTO public.attribute_type VALUES ('activity-id', 'string');
INSERT INTO public.attribute_type VALUES ('crs-channel-code', 'string');
INSERT INTO public.attribute_type VALUES ('code', 'string');
INSERT INTO public.attribute_type VALUES ('vocabulary-uri', 'string');
INSERT INTO public.attribute_type VALUES ('significance', 'string');
INSERT INTO public.attribute_type VALUES ('provider-activity-id', 'string');
INSERT INTO public.attribute_type VALUES ('receiver-activity-id', 'string');
INSERT INTO public.attribute_type VALUES ('ref', 'string');
INSERT INTO public.attribute_type VALUES ('srsName', 'string');
INSERT INTO public.attribute_type VALUES ('iati-equivalent', 'string');
INSERT INTO public.attribute_type VALUES ('indicator-uri', 'string');
INSERT INTO public.attribute_type VALUES ('measure', 'string');
INSERT INTO public.attribute_type VALUES ('status', 'string');
INSERT INTO public.attribute_type VALUES ('currency', 'string');
INSERT INTO public.attribute_type VALUES ('value-date', 'string');
INSERT INTO public.attribute_type VALUES ('vocabulary', 'string');
INSERT INTO public.attribute_type VALUES ('name', 'string');
INSERT INTO public.attribute_type VALUES ('value', 'string');
INSERT INTO public.attribute_type VALUES ('last-updated-datetime', 'date');
INSERT INTO public.attribute_type VALUES ('iso-date', 'date');
INSERT INTO public.attribute_type VALUES ('extraction-date', 'date');
INSERT INTO public.attribute_type VALUES ('humanitarian', 'boolean');
INSERT INTO public.attribute_type VALUES ('ascending', 'boolean');
INSERT INTO public.attribute_type VALUES ('aggregation-status', 'boolean');
INSERT INTO public.attribute_type VALUES ('attached', 'boolean');
INSERT INTO public.attribute_type VALUES ('priority', 'boolean');
INSERT INTO public.attribute_type VALUES ('hierarchy', 'numeric');
INSERT INTO public.attribute_type VALUES ('percentage', 'numeric');
INSERT INTO public.attribute_type VALUES ('level', 'numeric');
INSERT INTO public.attribute_type VALUES ('year', 'numeric');
INSERT INTO public.attribute_type VALUES ('rate-1', 'numeric');
INSERT INTO public.attribute_type VALUES ('rate-2', 'numeric');
INSERT INTO public.attribute_type VALUES ('phaseout-year', 'numeric');
INSERT INTO public.attribute_type VALUES ('format', 'string');
INSERT INTO public.attribute_type VALUES ('url', 'string');
INSERT INTO public.attribute_type VALUES ('secondary-reporter', 'boolean');

ALTER TABLE ONLY public.element
    ADD CONSTRAINT "Element_pkey" PRIMARY KEY (md5_pk);

ALTER TABLE ONLY public.attribute
    ADD CONSTRAINT attribute_pkey PRIMARY KEY (md5_pk);

ALTER TABLE ONLY public.attribute_type
    ADD CONSTRAINT attribute_type_pkey PRIMARY KEY (name);

ALTER TABLE ONLY public.element_to_attribute
    ADD CONSTRAINT e2a_compound_pkey PRIMARY KEY (element_key, attribute_key);

ALTER TABLE ONLY public.element_to_activity
    ADD CONSTRAINT e2act_compound_pkey PRIMARY KEY (element_key, activity_key);

ALTER TABLE ONLY public.element_to_child
    ADD CONSTRAINT e2c_compound_pkey PRIMARY KEY (element_key, child_key);

ALTER TABLE ONLY public.element_to_parent
    ADD CONSTRAINT e2p_compound_pkey PRIMARY KEY (element_key, parent_key);

ALTER TABLE ONLY public.refresher
    ADD CONSTRAINT refresher_pkey PRIMARY KEY (id);

CREATE INDEX el_name ON public.element USING btree (name);

CREATE INDEX fki_attribute_key ON public.element_to_attribute USING btree (attribute_key);

CREATE INDEX fki_e2ct_activty_key ON public.element_to_activity USING btree (activity_key);

CREATE INDEX fki_e2ct_element_key ON public.element_to_activity USING btree (element_key);

CREATE INDEX fki_element_key ON public.element_to_attribute USING btree (element_key);

CREATE INDEX fki_etc_child_key ON public.element_to_child USING btree (child_key);

CREATE INDEX fki_etc_element_key ON public.element_to_child USING btree (element_key);

CREATE INDEX fki_etp_element_key ON public.element_to_parent USING btree (element_key);

CREATE INDEX fki_etp_parent_key ON public.element_to_parent USING btree (parent_key);

CREATE INDEX fki_file_id ON public.refresher USING btree (id);

CREATE INDEX fki_file_hash ON public.refresher USING btree (hash);

CREATE INDEX fki_file_url ON public.refresher USING btree (url);

CREATE INDEX fki_file_root_element ON public.refresher USING btree (root_element_key);

CREATE INDEX name ON public.element USING gin (text_tokens);

CREATE INDEX str_val ON public.attribute USING btree (string_value);

ALTER TABLE ONLY public.element_to_attribute
    ADD CONSTRAINT attribute FOREIGN KEY (attribute_key) REFERENCES public.attribute(md5_pk);

ALTER TABLE ONLY public.attribute
    ADD CONSTRAINT attribute_type FOREIGN KEY (name) REFERENCES public.attribute_type(name);

ALTER TABLE ONLY public.element_to_activity
    ADD CONSTRAINT e2act_activity_key FOREIGN KEY (element_key) REFERENCES public.element(md5_pk);

ALTER TABLE ONLY public.element_to_activity
    ADD CONSTRAINT e2ct_element_key FOREIGN KEY (element_key) REFERENCES public.element(md5_pk);

ALTER TABLE ONLY public.element_to_attribute
    ADD CONSTRAINT element FOREIGN KEY (element_key) REFERENCES public.element(md5_pk);

ALTER TABLE ONLY public.element_to_child
    ADD CONSTRAINT element_to_child_key_fkey FOREIGN KEY (child_key) REFERENCES public.element(md5_pk);

ALTER TABLE ONLY public.element_to_child
    ADD CONSTRAINT element_to_element_key_fkey FOREIGN KEY (element_key) REFERENCES public.element(md5_pk);

ALTER TABLE ONLY public.element_to_parent
    ADD CONSTRAINT element_to_element_key_fkey FOREIGN KEY (element_key) REFERENCES public.element(md5_pk);

ALTER TABLE ONLY public.element_to_parent
    ADD CONSTRAINT element_to_parent_key_fkey FOREIGN KEY (parent_key) REFERENCES public.element(md5_pk);

ALTER TABLE ONLY public.refresher
    ADD CONSTRAINT file_root_element FOREIGN KEY (root_element_key) REFERENCES public.element(md5_pk) NOT VALID;

"""
