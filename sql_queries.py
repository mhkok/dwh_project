import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop  = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop       = "DROP TABLE IF EXISTS songplay"
user_table_drop           = "DROP TABLE IF EXISTS user"
song_table_drop           = "DROP TABLE IF EXISTS song"
artist_table_drop         = "DROP TABLE IF EXISTS artist"
time_table_drop           = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= (
    """
    CREATE TABLE staging_events (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender VARCHAR,
        itemInSession INT,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration FLOAT,
        sessionId INT,
        song VARCHAR,
        status INT,
        ts INT,
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
        songplay_id SERIAL PRIMARY KEY, 
        start_time BIGINT NOT NULL, 
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

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
