# Digital Konbini

## An Online Retail Store Management System
**Team:** Himang Chandra Garg, Nishil Agarwal, Prince Yadav, Tizil Sharma  
**Date:** January 2024

---

## Table of Contents
- [Scope](#scope)
- [Objectives](#objectives)
- [Stakeholders & Functionalities](#stakeholders--functionalities)
- [Constraints on Stakeholders](#constraints-on-stakeholders)
- [Tech Stack](#tech-stack)

---

## Scope
The project aims to develop a business-to-consumer (B2C) database application for an online retail store. The primary focus is crafting a robust back-end system that will efficiently manage and optimize the interactions between various data entities. The design will encompass a detailed selection of data entities, establishing relationships, and the imposition of constraints to ensure data integrity. This project addresses data duplication and concurrent access challenges while emphasizing the strong protection of crucial information. Additionally, the application will be demonstrated through a user-friendly front-end interface.

- **Vendors** are responsible for supplying the retail store with products and managing product information. They can extend special offers for their products and securely store their contact details. Vendors can also monitor their product sales.
- **Customers** can log in to their accounts, add products to their shopping carts, and remove items at their convenience by browsing various products available at the store. They can review recent orders and receive product suggestions based on previous purchases. Access to customer care and support services is also available.
- **Admins** serve as supervisors of the retail store. They inform vendors about products that are out of stock, review product details provided by vendors, and make informed decisions on purchases. Admins can manage and categorize products in the database and access profit/loss data. For enhanced security, their contact information is stored and utilized during the sign-in process.

---

## Objectives
- Define data entities such as Customers, Products, Orders, and Vendors.
- Establish relationships and constraints between these entities to ensure data integrity.
- Implement mechanisms for populating the database with fictional data.
- Develop a user-friendly GUI interface to facilitate seamless navigation, product search, and efficient order management.
- **Inventory Management**: Track product availability and update inventory levels. Notify vendors and admins when stock falls below a certain threshold.
- Implement password protection and account recovery mechanisms for all accounts to protect user data and transactions.
- Track sales data, generate sales reports, and provide insights for decision-making.

---

## Stakeholders & Functionalities

### Customers
- Register / Login
- View Account Details
- Browse Products
- Place Orders
- View Order History
- Manage their cart
- Access to Customer Support

### Vendors
- Register / Login
- View Account Details
- Allow Offers on Products
- Manage Product Information
- Track Product Sales

### Admin
- Access data of Customers
- Access data of Vendors
- Access Sales data of Products
- Manage Stock of Products
- Apply Discounts and Offers
- Manage Customer Support
- Add/Remove Products

---

## Constraints on Stakeholders
- **Customers**: Cannot change information of other users, products, or vendors.
- **Vendors**: Cannot access information of other vendors and customers.
- **Admin**: Cannot change information of customers or vendors.

---

## Tech Stack
- **Database**: MySQL
- **Front End**: HTML, CSS, JavaScript
- **Back End**: Python( PyMySQl, flask )
- **Tools**: Overleaf, VSCode
