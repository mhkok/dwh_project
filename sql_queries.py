import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop  = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop       = "DROP TABLE IF EXISTS songplay"
user_table_drop           = "DROP TABLE IF EXISTS users"
song_table_drop           = "DROP TABLE IF EXISTS songs"
artist_table_drop         = "DROP TABLE IF EXISTS artists"
time_table_drop           = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= (
    """
    CREATE TABLE staging_events (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender VARCHAR,
        itemInSession BIGINT,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration FLOAT,
        sessionId INT,
        song VARCHAR,
        status BIGINT,
        ts BIGINT,
        userAgent VARCHAR,
        userId INT
    );
    """
)

staging_songs_table_create = (
    """
    CREATE TABLE staging_songs (
        num_songs INT,
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR,
        title VARCHAR,
        duration FLOAT,
        year INT
    );
    """
)

songplay_table_create = (
    """
    CREATE TABLE songplay (
        songplay_id INT PRIMARY KEY, 
        start_time TIMESTAMP NOT NULL, 
        user_id INT,
        level VARCHAR(255), 
        song_id VARCHAR(255), 
        artist_id VARCHAR(255), 
        session_id INT, 
        location VARCHAR(255), 
        user_agent VARCHAR(255)
    );
    """
)

user_table_create = (
    """
    CREATE TABLE users (
        user_id INT NOT NULL PRIMARY KEY, 
        first_name VARCHAR(255), 
        last_name VARCHAR(255), 
        gender VARCHAR(255), 
        level VARCHAR(255)
    );
    """
)   

song_table_create = (
    """
    CREATE TABLE songs (
        song_id VARCHAR(255) NOT NULL PRIMARY KEY, 
        title VARCHAR(255) NOT NULL, 
        artist_id VARCHAR(255) NOT NULL, 
        year INT, 
        duration FLOAT
    );
    """
)

artist_table_create = (
    """
    CREATE TABLE artists (
        artist_id VARCHAR(255) NOT NULL PRIMARY KEY, 
        name VARCHAR(255), 
        location VARCHAR(255), 
        latitude FLOAT, 
        longitude FLOAT
    );
    """
)

time_table_create = (
    """
    CREATE TABLE time (
        start_time TIME NOT NULL PRIMARY KEY, 
        hour INT, 
        day INT, 
        week INT, 
        month INT, 
        year INT, 
        weekday INT
    );
    """
)

# STAGING TABLES

staging_songs_copy = (
    """
    COPY staging_songs from 's3://udacity-dend/song-data/A/A'
    CREDENTIALS 'aws_iam_role={}'
    region 'us-west-2' 
    JSON 'auto';
    """
    ).format(config.get('IAM_ROLE', 'ARN'))

staging_events_copy = (
    """
    COPY staging_events from 's3://udacity-dend/log-data'
    CREDENTIALS 'aws_iam_role={}'
    region 'us-west-2' compupdate OFF
    JSON 's3://udacity-dend/log_json_path.json';
    """
    ).format(config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = (
    """
    INSERT INTO songplay (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT  ss.song_id AS songplay_id
            ss.ts AS DATE
            ss.userid,
            ss.level,
            ss.song_id
            ss.artist_id
            ss.session
    FROM staging_songs ss
    JOIN staging_events se
    """
)

user_table_insert = (
    """
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT se.userid,
           se.firstname,
           se.lastname,
           se.gender,
           se.level
    FROM staging_events se
    WHERE userid IS NOT NULL
    """
)

song_table_insert = (
    """
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT  ss.song_id,
            ss.title,
            ss.artist_id,
            ss.year,
            ss.duration
    FROM staging_songs ss
    """
)

artist_table_insert = (
    """
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT  ss.artist_id,
            ss.artist_name,
            ss.artist_location,
            ss.artist_latitude,
            ss.artist_longitude
    FROM staging_songs ss
    """
)

time_table_insert = (
    """
    INSERT  INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT  DISTINCT start_time,
            EXTRACT (hour FROM start_time) AS hour,
            EXTRACT (day FROM start_time) AS day,
            EXTRACT (week FROM start_time) AS week,
            EXTRACT (month FROM start_time) AS month,
            EXTRACT (year FROM start_time) AS year,
            EXTRACT (weekday FROM start_time) AS weekday
    FROM (SELECT TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 Second' as start_time FROM staging_events se)
    """
)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
