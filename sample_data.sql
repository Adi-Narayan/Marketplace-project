-- Sample data for the Jewelry Marketplace Database

-- Sample Categories
INSERT INTO Categories (name) VALUES 
('Rings'),
('Necklaces'),
('Earrings'),
('Bracelets'),
('Watches');

-- Sample Users
INSERT INTO Users (username, password, email, firstname, lastname, address, phone) VALUES 
('johndoe', 'hashed_password_1', 'john.doe@example.com', 'John', 'Doe', '123 Main St, Anytown, CA 94121', '555-123-4567'),
('janedoe', 'hashed_password_2', 'jane.doe@example.com', 'Jane', 'Doe', '456 Oak Ave, Sometown, NY 10001', '555-987-6543'),
('msmith', 'hashed_password_3', 'mike.smith@example.com', 'Michael', 'Smith', '789 Pine Rd, Othertown, TX 75001', '555-456-7890'),
('agarcia', 'hashed_password_4', 'anna.garcia@example.com', 'Anna', 'Garcia', '321 Elm Blvd, Newtown, FL 33101', '555-234-5678'),
('bjohnson', 'hashed_password_5', 'bob.johnson@example.com', 'Robert', 'Johnson', '654 Maple Ln, Oldtown, WA 98101', '555-876-5432');

-- Sample Products
INSERT INTO Products (name, description, price, stock_quantity, category_id) VALUES 
('Diamond Solitaire Ring', '1 carat diamond in platinum setting', 3999.99, 10, 1),
('Pearl Necklace', '18-inch strand of cultured pearls', 899.99, 15, 2),
('Sapphire Stud Earrings', '0.5 carat each in 14k gold', 599.99, 20, 3),
('Gold Tennis Bracelet', '14k gold with 2 carats of diamonds', 2499.99, 8, 4),
('Silver Luxury Watch', 'Swiss movement with sapphire crystal', 1499.99, 12, 5),
('Ruby Engagement Ring', '0.75 carat ruby with diamond accents', 1299.99, 7, 1),
('Gold Chain Necklace', '20-inch 18k gold chain', 799.99, 18, 2),
('Diamond Hoop Earrings', '0.25 carats total in 14k white gold', 499.99, 25, 3),
('Silver Charm Bracelet', 'Sterling silver with 5 charms', 199.99, 30, 4),
('Rose Gold Watch', 'Automatic movement with leather band', 899.99, 10, 5);

-- Sample Sets
INSERT INTO Sets (name, description, price, stock_quantity) VALUES 
('Wedding Collection', 'Complete set of bridal jewelry', 4999.99, 5),
('Evening Elegance', 'Perfect for formal events', 3499.99, 8),
('Everyday Essentials', 'Versatile pieces for daily wear', 1299.99, 15),
('Vintage Inspired', 'Classic designs with modern craftsmanship', 2499.99, 6),
('Modern Minimalist', 'Clean lines and contemporary styling', 1799.99, 10);

-- Sample Set_Items (junction table entries)
INSERT INTO Set_Items (set_id, product_id) VALUES
(1, 1), -- Wedding Collection includes Diamond Solitaire Ring
(1, 2), -- Wedding Collection includes Pearl Necklace
(1, 3), -- Wedding Collection includes Sapphire Stud Earrings
(2, 6), -- Evening Elegance includes Ruby Engagement Ring
(2, 7), -- Evening Elegance includes Gold Chain Necklace
(3, 8), -- Everyday Essentials includes Diamond Hoop Earrings
(3, 9), -- Everyday Essentials includes Silver Charm Bracelet
(4, 2), -- Vintage Inspired includes Pearl Necklace
(4, 6), -- Vintage Inspired includes Ruby Engagement Ring
(5, 8), -- Modern Minimalist includes Diamond Hoop Earrings
(5, 10); -- Modern Minimalist includes Rose Gold Watch

-- Sample Orders
INSERT INTO Orders (user_id, order_date, total_amount, status) VALUES 
(1, '2025-03-15 10:30:00', 4599.98, 'delivered'),
(2, '2025-03-20 14:45:00', 799.99, 'shipped'),
(3, '2025-04-01 09:15:00', 4999.99, 'pending'),
(4, '2025-04-05 16:20:00', 699.98, 'shipped'),
(5, '2025-04-10 11:05:00', 1799.99, 'pending');

-- Sample Order_Items
INSERT INTO Order_Items (order_id, product_id, set_id, quantity, unit_price) VALUES 
(1, 1, NULL, 1, 3999.99), -- John ordered 1 Diamond Solitaire Ring
(1, 3, NULL, 1, 599.99), -- John also ordered 1 Sapphire Stud Earrings
(2, 7, NULL, 1, 799.99), -- Jane ordered 1 Gold Chain Necklace
(3, NULL, 1, 1, 4999.99), -- Michael ordered 1 Wedding Collection set
(4, 8, NULL, 1, 499.99), -- Anna ordered 1 Diamond Hoop Earrings
(4, 9, NULL, 1, 199.99), -- Anna also ordered 1 Silver Charm Bracelet
(5, NULL, 5, 1, 1799.99); -- Robert ordered 1 Modern Minimalist set

-- Sample Reviews
INSERT INTO Reviews (user_id, product_id, set_id, rating, comment, created_at) VALUES 
(1, 1, NULL, 5, 'Beautiful ring, exactly as described. My fiancée loves it!', '2025-03-20 15:10:00'),
(2, 7, NULL, 4, 'Great quality chain, but slightly shorter than expected.', '2025-03-25 09:45:00'),
(3, NULL, 1, 5, 'Perfect set for our wedding. Highly recommend.', '2025-04-10 14:30:00'),
(4, 8, NULL, 3, 'Nice earrings but one of the backings was loose.', '2025-04-12 17:20:00'),
(5, NULL, 5, 5, 'Stylish and modern. Get compliments every time I wear it.', '2025-04-15 10:55:00');

-- Sample Payments
INSERT INTO Payments (order_id, amount, payment_method, payment_status, transaction_id, payment_date) VALUES 
(1, 4599.98, 'credit card', 'completed', 'txn_123456789', '2025-03-15 10:35:00'),
(2, 799.99, 'PayPal', 'completed', 'txn_234567890', '2025-03-20 14:48:00'),
(3, 4999.99, 'credit card', 'completed', 'txn_345678901', '2025-04-01 09:18:00'),
(4, 699.98, 'PayPal', 'completed', 'txn_456789012', '2025-04-05 16:23:00'),
(5, 1799.99, 'credit card', 'pending', NULL, '2025-04-10 11:08:00');