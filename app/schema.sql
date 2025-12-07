-- ============================
-- Image Table
-- ============================
CREATE TABLE
    `image` (
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(255) NOT NULL UNIQUE,
        `data` LONGBLOB NOT NULL,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ============================
-- Location Table
-- ============================
CREATE TABLE
    location (
        sId INT AUTO_INCREMENT PRIMARY KEY,
        -- Coordinate
        latitude DECIMAL(10, 7) NOT NULL,
        longitude DECIMAL(10, 7) NOT NULL,
        -- Address
        city VARCHAR(100) NOT NULL,
        address VARCHAR(255) NOT NULL,
        zipcode VARCHAR(20) NOT NULL,
        -- Opening Hours
        mon TINYINT (1) NOT NULL DEFAULT 0,
        tue TINYINT (1) NOT NULL DEFAULT 0,
        wed TINYINT (1) NOT NULL DEFAULT 0,
        thu TINYINT (1) NOT NULL DEFAULT 0,
        fri TINYINT (1) NOT NULL DEFAULT 0,
        sat TINYINT (1) NOT NULL DEFAULT 0,
        sun TINYINT (1) NOT NULL DEFAULT 0,
        open_time TIME NOT NULL,
        close_time TIME NOT NULL
    );

-- ============================
-- Employee Table
-- ============================
CREATE TABLE
    employee (
        eId INT AUTO_INCREMENT PRIMARY KEY,
        -- Basic Info
        name VARCHAR(100) NOT NULL,
        position VARCHAR(100) NOT NULL,
        -- Contact
        email VARCHAR(100) NOT NULL,
        phone VARCHAR(50),
        -- Work Location
        store INT NULL,
        FOREIGN KEY (store) REFERENCES location (sId) ON DELETE SET NULL,
        -- Hire Information
        hireDate DATE,
        type VARCHAR(20)
    );

-- ============================
-- Supplier Table
-- ============================
CREATE TABLE
    `supplier` (
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        -- Basic Info
        `name` VARCHAR(100) NOT NULL UNIQUE,
        `description` TEXT,
        -- Contact
        `contact_person` VARCHAR(100),
        `email` VARCHAR(100) UNIQUE,
        `phone` VARCHAR(30) UNIQUE,
        -- Address
        `state` VARCHAR(100),
        `city` VARCHAR(100),
        `address` VARCHAR(255),
        -- Others
        `image_url` VARCHAR(255),
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ============================
-- Ingredient Table
-- ============================
CREATE TABLE
    `ingredient` (
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(100) NOT NULL UNIQUE,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ============================
-- Dish Table
-- ============================
CREATE TABLE
    `dish` (
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(100) NOT NULL UNIQUE,
        `description` TEXT,
        `price` DECIMAL(10, 2) NOT NULL,
        `calories` INT,
        `image_url` VARCHAR(255),
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ============================
-- Combo Table
-- ============================
CREATE TABLE
    `combo` (
        `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(100) NOT NULL UNIQUE,
        `description` TEXT,
        `price` DECIMAL(10, 2) NOT NULL,
        `image_url` VARCHAR(255),
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ============================
-- associative Tables
-- Suppliers & Ingredients & Dishes & Combos
-- ============================
CREATE TABLE
    `supplier_ingredient` (
        `supplier_id` INT UNSIGNED,
        `ingredient_id` INT UNSIGNED,
        PRIMARY KEY (`supplier_id`, `ingredient_id`),
        FOREIGN KEY (`supplier_id`) REFERENCES `supplier` (`id`) ON DELETE CASCADE,
        FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    `dish_ingredient` (
        `dish_id` INT UNSIGNED,
        `ingredient_id` INT UNSIGNED,
        `quantity` DECIMAL(10, 2) NOT NULL,
        `unit` VARCHAR(50) NOT NULL,
        PRIMARY KEY (`dish_id`, `ingredient_id`),
        FOREIGN KEY (`dish_id`) REFERENCES `dish` (`id`) ON DELETE CASCADE,
        FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE
    `combo_dish` (
        `combo_id` INT UNSIGNED,
        `dish_id` INT UNSIGNED,
        PRIMARY KEY (`combo_id`, `dish_id`),
        FOREIGN KEY (`combo_id`) REFERENCES `combo` (`id`) ON DELETE CASCADE,
        FOREIGN KEY (`dish_id`) REFERENCES `dish` (`id`) ON DELETE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;