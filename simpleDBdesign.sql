CREATE SCHEMA 'aircargo';

CREATE TABLE 'aircargo'.'customer' (
  'id' int PRIMARY KEY,
  'first_name' varchar(50),
  'last_name' varchar(50),
  'date_of_birth' date,
  'gender' char(1)
);

CREATE TABLE 'aircargo'.'airport' (
  'id' char(3) PRIMARY KEY,
  'name' varchar(200),
  'city' varchar(100),
  'state_prov' varchar(5),
  'country' varchar(25)
);

CREATE TABLE 'aircargo'.'aircraft' (
  'id' varchar(25) PRIMARY KEY,
  'manufacturer' varchar(50)
);

CREATE TABLE 'aircargo'.'routes' (
  'route_id' int PRIMARY KEY,
  'flight_num' int,
  'origin_airport' char(3),
  'destination_airport' char(3),
  'aircraft_id' varchar(25),
  'distance_miles' int
);

CREATE TABLE 'aircargo'.'passengers_on_flight' (
  'customer_id' int,
  'aircraft_id' varchar(25),
  'route_id' int,
  'depart' char(3),
  'arrival' char(3),
  'seat_num' varchar(10),
  'class_id' varchar(50),
  'travel_date' date,
  'flight_num' int
);

CREATE TABLE 'aircargo'.'ticket_details' (
  'p_date' date,
  'customer_id' int,
  'aircraft_id' varchar(25),
  'class_id' varchar(50),
  'no_of_tickets' int,
  'a_code' char(3),
  'Price_per_ticket' int,
  'brand' varchar(100)
);

ALTER TABLE 'aircargo'.'routes' ADD FOREIGN KEY ('origin_airport') REFERENCES 'aircargo'.'airport' ('id');

ALTER TABLE 'aircargo'.'routes' ADD FOREIGN KEY ('destination_airport') REFERENCES 'aircargo'.'airport' ('id');

ALTER TABLE 'aircargo'.'routes' ADD FOREIGN KEY ('aircraft_id') REFERENCES 'aircargo'.'aircraft' ('id');

ALTER TABLE 'aircargo'.'passengers_on_flight' ADD FOREIGN KEY ('customer_id') REFERENCES 'aircargo'.'customer' ('id');

ALTER TABLE 'aircargo'.'passengers_on_flight' ADD FOREIGN KEY ('aircraft_id') REFERENCES 'aircargo'.'aircraft' ('id');

ALTER TABLE 'aircargo'.'passengers_on_flight' ADD FOREIGN KEY ('route_id') REFERENCES 'aircargo'.'routes' ('route_id');

ALTER TABLE 'aircargo'.'passengers_on_flight' ADD FOREIGN KEY ('depart') REFERENCES 'aircargo'.'airport' ('id');

ALTER TABLE 'aircargo'.'passengers_on_flight' ADD FOREIGN KEY ('arrival') REFERENCES 'aircargo'.'airport' ('id');

ALTER TABLE 'aircargo'.'ticket_details' ADD FOREIGN KEY ('customer_id') REFERENCES 'aircargo'.'customer' ('id');

ALTER TABLE 'aircargo'.'ticket_details' ADD FOREIGN KEY ('aircraft_id') REFERENCES 'aircargo'.'aircraft' ('id');

ALTER TABLE 'aircargo'.'ticket_details' ADD FOREIGN KEY ('a_code') REFERENCES 'aircargo'.'airport' ('id');
