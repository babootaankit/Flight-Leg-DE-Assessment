--Query to dedup flightkey and choose most up to date record
SELECT a.flightkey,
       a.flightnum,
       a.flight_dt,
       a.orig_arpt,
       a.dest_arpt,
       a.flightstatus,
       a.lastupdt
FROM flight_leg a
JOIN (
    SELECT flightkey, MAX(lastupdt) AS latest_dt
    FROM flight_leg
    GROUP BY flightkey
) b
ON a.flightkey = b.flightkey
AND a.lastupdt = b.latest_dt;