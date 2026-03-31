-- Run this SQL in your Supabase SQL Editor to create the users table

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
  user_id       UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
  fullname      TEXT        NOT NULL,
  age           INTEGER     NOT NULL CHECK (age > 0),
  address       TEXT        NOT NULL,
  phone_number  TEXT        NOT NULL,
  email         TEXT        NOT NULL UNIQUE,
  shirt_size    TEXT        NOT NULL CHECK (shirt_size IN ('XS', 'S', 'M', 'L', 'XL', '2XL', '3XL')),
  distance      TEXT        NOT NULL DEFAULT '5KM' CHECK (distance IN ('5KM', '10KM', '15KM')),
  payment_status TEXT       NOT NULL DEFAULT 'pending' CHECK (payment_status IN ('pending', 'waiting_verification', 'paid', 'failed')),
  slip_url      TEXT        DEFAULT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
