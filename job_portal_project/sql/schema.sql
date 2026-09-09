CREATE DATABASE IF NOT EXISTS jobportal;

USE jobportal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100),
    mobile VARCHAR(20),
    password VARCHAR(100)
);

CREATE TABLE job_applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100),
    mobile VARCHAR(20),
    qualification VARCHAR(100),
    skills VARCHAR(100),
    experience VARCHAR(100),
    resume_url TEXT,
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
