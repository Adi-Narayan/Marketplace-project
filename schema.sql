-- Database Schema for Jewelry Marketplace

-- Create the Users table
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20) NOT NULL
);

-- Create the Categories table
CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Create the Products table
CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);

-- Create the Sets table
CREATE TABLE Sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL
);

-- Create the Set_Items junction table for Sets and Products
CREATE TABLE Set_Items (
    set_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    PRIMARY KEY (set_id, product_id),
    FOREIGN KEY (set_id) REFERENCES Sets(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

-- Create the Orders table
CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK(status IN ('pending', 'shipped', 'delivered')),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create the Order_Items table
CREATE TABLE Order_Items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER,
    set_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    FOREIGN KEY (set_id) REFERENCES Sets(id),
    CHECK (
        (product_id IS NOT NULL AND set_id IS NULL) OR 
        (product_id IS NULL AND set_id IS NOT NULL)
    )
);

-- Create the Reviews table
CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER,
    set_id INTEGER,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (product_id) REFERENCES Products(id),
    FOREIGN KEY (set_id) REFERENCES Sets(id),
    CHECK (
        (product_id IS NOT NULL AND set_id IS NULL) OR 
        (product_id IS NULL AND set_id IS NOT NULL)
    )
);

-- Create the Payments table
CREATE TABLE Payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL UNIQUE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(20) NOT NULL CHECK(payment_status IN ('pending', 'completed', 'failed')),
    transaction_id VARCHAR(100),
    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(id)
);

-- Create indexes for performance
CREATE INDEX idx_products_category ON Products(category_id);
CREATE INDEX idx_order_items_order ON Order_Items(order_id);
CREATE INDEX idx_order_items_product ON Order_Items(product_id);
CREATE INDEX idx_order_items_set ON Order_Items(set_id);
CREATE INDEX idx_reviews_user ON Reviews(user_id);
CREATE INDEX idx_reviews_product ON Reviews(product_id);
CREATE INDEX idx_reviews_set ON Reviews(set_id);
CREATE INDEX idx_orders_user ON Orders(user_id);
CREATE INDEX idx_set_items_set ON Set_Items(set_id);
CREATE INDEX idx_set_items_product ON Set_Items(product_id);