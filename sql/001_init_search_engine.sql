-- ============================================
-- Database: search_engine
-- Description: Schema definitions for search engine system
-- ============================================

-- Create the database
CREATE DATABASE IF NOT EXISTS `search_engine`;
USE `search_engine`;

-- ============================================
-- Table: search_schemas
-- Description: Stores schema definitions used in Redis search indices
-- ============================================

CREATE TABLE `search_schemas` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `redis_index_name` VARCHAR(255) NOT NULL UNIQUE,
    `fields` JSON NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
