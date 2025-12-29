create database the_mill;
use the_mill;



#employee_table
create table employee(
emp_id int primary key,
emp_name varchar(50),
role varchar(20)

);

INSERT INTO employee (emp_id, emp_name, role) VALUES (1, 'Tanisha', 'Manager');
INSERT INTO employee (emp_id, emp_name, role) VALUES (2, 'Ujjwal', 'Chef');
INSERT INTO employee (emp_id, emp_name, role) VALUES (3, 'Sahil', 'Waiter');

-- Order table
create table orders(
token_no int auto_increment primary key,
waiter_id int,
table_no int,
order_date date,
status varchar (20)

);

-- Order Items Table
create table order_items(
item_id int auto_increment primary key,
token_no int,
food_code int,
quantity int,
foreign key (token_no) references orders(token_no),
foreign key (food_code) references menu(food_code)

);

-- Billing Table
CREATE TABLE billing (
bill_id INT AUTO_INCREMENT PRIMARY KEY,
token_no INT,
subtotal DECIMAL(10,2),
gst DECIMAL(10,2),
total_amount DECIMAL(10,2),
bill_date DATE,
FOREIGN KEY (token_no) REFERENCES orders(token_no)
);

-- Menu Table
CREATE TABLE menu (
    food_code INT PRIMARY KEY,
    food_name VARCHAR(50),
    price DECIMAL(10,2)
);

INSERT INTO menu VALUES
(201, 'Classic Cappuccino', 160.00),
(202, 'Cafe Latte', 150.00),
(203, 'Espresso Shot', 120.00),
(204, 'Cold Brew Coffee', 180.00),
(205, 'Chocolate Brownie', 140.00),
(206, 'Blueberry Cheesecake', 220.00),
(207, 'Grilled Veg Sandwich', 190.00),
(208, 'Paneer Panini', 210.00),
(209, 'French Fries', 130.00),
(210, 'Masala Chai', 90.00),
(211, 'Iced Lemon Tea', 120.00),
(212, 'Veg Club Sandwich', 230.00);

select * from employee;
select * from menu;
select * from billing;
select * from orders;
select * from order_items;
drop table users;



