-- Insert sample data into Users table
INSERT INTO Users (username, password, email, firstname, lastname, address, phone) VALUES
('admin', 'admin123', 'admin@jewelrymarket.com', 'Admin', 'User', '123 Admin St, Jewel City, JC 12345', '555-0100'),
('johndoe', 'pass123', 'john.doe@gmail.com', 'John', 'Doe', '456 Maple Ave, Jewel City, JC 12345', '555-0101'),
('janedoe', 'secure456', 'jane.doe@yahoo.com', 'Jane', 'Doe', '789 Oak St, Jewel City, JC 12345', '555-0102'),
('alicew', 'alice789', 'alice.wilson@outlook.com', 'Alice', 'Wilson', '321 Pine Rd, Jewel City, JC 12345', '555-0103'),
('bobsmith', 'bob101', 'bob.smith@gmail.com', 'Bob', 'Smith', '654 Elm St, Jewel City, JC 12345', '555-0104'),
('carolb', 'carol202', 'carol.brown@protonmail.com', 'Carol', 'Brown', '987 Birch Ln, Jewel City, JC 12345', '555-0105'),
('davidm', 'david303', 'david.miller@icloud.com', 'David', 'Miller', '147 Cedar Dr, Jewel City, JC 12345', '555-0106'),
('emilyt', 'emily404', 'emily.taylor@aol.com', 'Emily', 'Taylor', '258 Spruce Way, Jewel City, JC 12345', '555-0107'),
('frankg', 'frank505', 'frank.green@gmail.com', 'Frank', 'Green', '369 Willow Ct, Jewel City, JC 12345', '555-0108'),
('graceh', 'grace606', 'grace.hall@yahoo.com', 'Grace', 'Hall', '741 Aspen Blvd, Jewel City, JC 12345', '555-0109');

-- Insert sample data into HashedPasswords table (SHA-256 hashes)
INSERT INTO HashedPasswords (user_id, hashed_password) VALUES
(1, '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'),
(2, '32250170a0dca92d53ec9624f336ca24c8d3f5d8e9bd08eb7e731d0a3e7f350b'),
(3, '6b09c3f27dbad593e04a738c87d699bb80a6ae3f8737e3c0d9189e744d6968c7'),
(4, 'c53ab6d602c770785b7b58ae4f79ab1b4c7b91f8c7b7be6d7e2eb146f8e2ad6d'),
(5, '3cc3f7576ef194b2a433ca1803ff9f9bed3ec1f9b9f11404a5f4e3071e023adc'),
(6, 'd5e29f8f8e7ed5235ab27e3f2a9cd6352b0ac41c4b2d7a34b8d5d5e7a5e5f5e5'),
(7, '6e7b2e9f5f7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f'),
(8, '7f8e9f5f7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e'),
(9, '8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e'),
(10, '9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f9e7f8e8f');

-- Insert sample data into Categories table
INSERT INTO Categories (name) VALUES
('Rings'),
('Necklaces'),
('Bracelets'),
('Earrings'),
('Pendants');

-- Insert sample data into Products table
INSERT INTO Products (name, description, price, stock_quantity, category_id) VALUES
('Diamond Solitaire Ring', '1-carat diamond in 14k white gold', 999.99, 10, 1),
('Emerald Band', 'Emerald stones in sterling silver', 299.99, 15, 1),
('Gold Chain Necklace', '18-inch 14k gold chain', 499.99, 20, 2),
('Pearl Pendant', 'Freshwater pearl on silver chain', 199.99, 25, 2),
('Tennis Bracelet', 'Cubic zirconia in sterling silver', 349.99, 12, 3),
('Charm Bracelet', 'Silver charm bracelet with heart pendant', 149.99, 18, 3),
('Hoop Earrings', '14k gold 1-inch hoop earrings', 249.99, 30, 4),
('Stud Earrings', 'Diamond studs in white gold', 399.99, 8, 4),
('Cross Pendant', '14k gold cross pendant', 179.99, 22, 5),
('Heart Locket', 'Sterling silver heart-shaped locket', 129.99, 28, 5),
('Sapphire Ring', 'Blue sapphire in white gold', 799.99, 5, 1),
('Opal Necklace', 'Opal stone on gold chain', 599.99, 10, 2),
('Bangle Bracelet', 'Solid gold bangle', 699.99, 7, 3),
('Drop Earrings', 'Emerald drop earrings', 449.99, 15, 4),
('Star Pendant', 'Star-shaped diamond pendant', 279.99, 20, 5);

-- Insert sample data into Sets table
INSERT INTO Sets (name, description, price, stock_quantity) VALUES
('Bridal Set', 'Diamond ring and matching band', 1499.99, 5),
('Pearl Collection', 'Pearl necklace and earrings', 799.99, 8),
('Gold Trio', 'Necklace, bracelet, and earrings', 999.99, 6),
('Gemstone Set', 'Sapphire ring and earrings', 1299.99, 4),
('Silver Elegance', 'Silver necklace and pendant', 499.99, 10);

-- Insert sample data into Set_Items table
INSERT INTO Set_Items (set_id, product_id) VALUES
(1, 1), (1, 2), -- Bridal Set: Diamond Solitaire Ring, Emerald Band
(2, 4), (2, 8), -- Pearl Collection: Pearl Pendant, Stud Earrings
(3, 3), (3, 6), (3, 7), -- Gold Trio: Gold Chain Necklace, Charm Bracelet, Hoop Earrings
(4, 11), (4, 14), -- Gemstone Set: Sapphire Ring, Drop Earrings
(5, 4), (5, 10); -- Silver Elegance: Pearl Pendant, Heart Locket

-- Insert sample data into Orders table
INSERT INTO Orders (user_id, order_date, total_amount, status) VALUES
(2, '2025-04-01 10:00:00', 1349.97, 'delivered'),
(3, '2025-04-02 12:30:00', 499.99, 'shipped'),
(4, '2025-04-03 15:45:00', 799.99, 'pending'),
(5, '2025-04-05 09:20:00', 2299.98, 'delivered'),
(6, '2025-04-07 14:10:00', 649.98, 'shipped'),
(7, '2025-04-10 11:25:00', 999.99, 'pending'),
(8, '2025-04-12 16:50:00', 1799.98, 'delivered'),
(9, '2025-04-15 08:30:00', 349.99, 'shipped'),
(10, '2025-04-18 13:40:00', 1299.99, 'pending'),
(2, '2025-04-20 10:15:00', 599.99, 'pending');

-- Insert sample data into Order_Items table
INSERT INTO Order_Items (order_id, product_id, set_id, quantity, unit_price) VALUES
(1, 1, NULL, 1, 999.99), (1, 6, NULL, 2, 149.99),
(2, NULL, 5, 1, 499.99),
(3, NULL, 2, 1, 799.99),
(4, 3, NULL, 2, 499.99), (4, 11, NULL, 1, 799.99),
(5, 7, NULL, 2, 249.99), (5, 8, NULL, 1, 399.99),
(6, NULL, 3, 1, 999.99),
(7, 1, NULL, 1, 999.99), (7, NULL, 1, 1, 1499.99),
(8, 5, NULL, 1, 349.99),
(9, NULL, 4, 1, 1299.99),
(10, 12, NULL, 1, 599.99);

-- Insert sample data into Reviews table
INSERT INTO Reviews (user_id, product_id, set_id, rating, comment, created_at) VALUES
(2, 1, NULL, 5, 'Stunning diamond ring, worth every penny!', '2025-04-02 08:00:00'),
(3, NULL, 5, 4, 'Beautiful silver set, great quality.', '2025-04-03 09:15:00'),
(4, NULL, 2, 5, 'The pearls are gorgeous!', '2025-04-04 10:30:00'),
(5, 3, NULL, 3, 'Nice necklace but clasp feels weak.', '2025-04-06 11:45:00'),
(6, 7, NULL, 4, 'Love these hoop earrings, very stylish.', '2025-04-08 13:00:00'),
(7, NULL, 3, 5, 'Perfect gold set for special occasions.', '2025-04-11 14:20:00'),
(8, 1, NULL, 5, 'My fiancee loves this ring!', '2025-04-13 15:40:00'),
(9, 5, NULL, 4, 'Great bracelet, fits perfectly.', '2025-04-16 16:55:00'),
(10, NULL, 4, 5, 'Sapphire set is breathtaking.', '2025-04-19 18:10:00'),
(2, 12, NULL, 4, 'Opal necklace is unique and lovely.', '2025-04-21 09:25:00');

-- Insert sample data into Payments table
INSERT INTO Payments (order_id, amount, payment_method, payment_status, transaction_id, payment_date) VALUES
(1, 1349.97, 'credit_card', 'completed', 'TXN123456789', '2025-04-01 10:05:00'),
(2, 499.99, 'paypal', 'completed', 'TXN234567890', '2025-04-02 12:35:00'),
(3, 799.99, 'credit_card', 'pending', 'TXN345678901', '2025-04-03 15:50:00'),
(4, 2299.98, 'credit_card', 'completed', 'TXN456789012', '2025-04-05 09:25:00'),
(5, 649.98, 'paypal', 'completed', 'TXN567890123', '2025-04-07 14:15:00'),
(6, 999.99, 'credit_card', 'pending', 'TXN678901234', '2025-04-10 11:30:00'),
(7, 1799.98, 'credit_card', 'completed', 'TXN789012345', '2025-04-12 16:55:00'),
(8, 349.99, 'paypal', 'completed', 'TXN890123456', '2025-04-15 08:35:00'),
(9, 1299.99, 'credit_card', 'pending', 'TXN901234567', '2025-04-18 13:45:00'),
(10, 599.99, 'credit_card', 'pending', 'TXN012345678', '2025-04-20 10:20:00');