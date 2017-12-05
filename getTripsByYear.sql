select year(date), sum(distance) from trips_trip group by year(date);
