CREATE VIEW geotweets AS (
    SELECT tw.id,
        tw.text,
        tw.timestamp,
        tw.lon,
        tw.lat,
        tw.user_id,
        tw.rtwts,
        tw.fvrts,
        tw.application,
        tracts.ct
    FROM tweets AS tw
    JOIN census_tracts AS tracts
    ON ST_Contains(tracts.wkb_geometry, ST_MakePoint(tw.lon, tw.lat, 4326))
);