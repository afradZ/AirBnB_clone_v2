DROP TABLE IF EXISTS places;

CREATE TABLE places (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    city_id VARCHAR(60) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(1024),
    number_rooms INT DEFAULT 0,
    number_bathrooms INT DEFAULT 0,
    max_guest INT DEFAULT 0,
    price_by_night INT DEFAULT 0,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (city_id) REFERENCES cities (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
