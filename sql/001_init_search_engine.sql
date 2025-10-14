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

-- ============================================
-- Table: search_logs
-- Description: Stores logs of Redis search queries, including parameters and execution time
-- ============================================

CREATE TABLE `search_logs` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `redis_index_name` VARCHAR(255) NOT NULL,
    `parameters` JSON NOT NULL,
    `duration_ms` INT NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_redis_index_name` (`redis_index_name`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
