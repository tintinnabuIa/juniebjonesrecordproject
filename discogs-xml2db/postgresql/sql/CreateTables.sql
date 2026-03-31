--- artists
CREATE TABLE artist (
    id              integer,
    name            text,
    realname        text,
    profile         text,

    data_quality    text
);

CREATE TABLE artist_url (
    id              SERIAL,
    artist_id       integer,
    url             text
);

CREATE TABLE artist_namevariation (
    id              SERIAL,
    artist_id       integer,
    name            text
);

CREATE TABLE artist_alias (
    artist_id       integer,
    alias_name      text,
    alias_artist_id integer
);

CREATE TABLE artist_image (
    artist_id       integer,
    type            text,
    width           integer,
    height          integer
);

CREATE TABLE group_member (
    group_artist_id     integer,
    member_artist_id    integer,
    member_name         text
);

--- labels
CREATE TABLE label (
    id              integer,
    name            text,
    contact_info    text,
    profile         text,
    parent_id       integer,
    parent_name     text,
    data_quality    text
);

CREATE TABLE label_url (
    id              SERIAL,
    label_id        integer,
    url             text
);

CREATE TABLE label_image (
    label_id        integer,
    type            text,
    width           integer,
    height          integer
);

--- masters
CREATE TABLE master (
    id              integer,
    title           text,
    year            integer,
    main_release    integer,
    data_quality    text
);

CREATE TABLE master_artist (
    id              SERIAL,
    master_id       integer,
    artist_id       integer,
    artist_name     text,
    anv             text,
    position        integer,
    join_string     text,
    role            text
);

CREATE TABLE master_video (
    id              SERIAL,
    master_id       integer,
    duration        integer,
    title           text,
    description     text,
    uri             text
);

CREATE TABLE master_genre (
    id              SERIAL,
    master_id       integer,
    genre           text
);

CREATE TABLE master_style (
    id              SERIAL,
    master_id       integer,
    style           text
);

CREATE TABLE master_image (
    master_id       integer,
    type            text,
    width           integer,
    height          integer
);

--- releases
CREATE TABLE release (
    id              integer,
    title           text,
    released        text,
    country         text,
    notes           text,
    data_quality    text,
    main            integer,
    master_id       integer,
    status          text
);

CREATE TABLE release_artist (
    id              SERIAL,
    release_id      integer,
    artist_id       integer,
    artist_name     text,
    extra           integer,
    anv             text,
    position        integer,
    join_string     text,
    role            text,
    tracks          text
);

CREATE TABLE release_label (
    id              SERIAL,
    release_id      integer,
    label_id        integer,
    label_name      text,
    catno           text
);

CREATE TABLE release_genre (
    id              SERIAL,
    release_id      integer,
    genre           text
);

CREATE TABLE release_style (
    release_id      integer,
    style           text
);

CREATE TABLE release_format (
    id              SERIAL,
    release_id      integer,
    name            text,
    qty             NUMERIC, -- There's 1 example e.g. 8262262,File,1000000000000000000000000000000000000000000000000000000000000001,32 kbps,MP3; Album; Mono
    text_string     text,
    descriptions    text
);

CREATE TABLE release_track (
    id              SERIAL,
    release_id      integer,
    sequence        integer,
    position        text,
    parent          text,
    title           text,
    duration        text,
    track_id        text
);

CREATE TABLE release_track_artist (
    id              SERIAL,
    track_id        text,
    release_id      integer,
    track_sequence  text,
    artist_id       integer,
    artist_name     text,
    extra           boolean,
    anv             text,
    position        integer,
    join_string     text,
    role            text,
    tracks          text
);

CREATE TABLE release_identifier (
    id              SERIAL,
    release_id      integer,
    description     text,
    type            text,
    value           text
);

CREATE TABLE release_video (
    id              SERIAL,
    release_id      integer,
    duration        integer,
    title           text,
    description     text,
    uri             text
);

CREATE TABLE release_company (
    id                  SERIAL,
    release_id          integer,
    company_id          integer,
    company_name        text,
    entity_type         text,
    entity_type_name    text,
    uri                 text
); 

CREATE TABLE release_image (
    release_id      integer,
    type            text,
    width           integer,
    height          integer
);

