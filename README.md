# SO Multiple DO (so_multiple_delivery)

## Overview

This module augments Odoo 17 by integrating the Sale Order and Stock Picking models. It adds the feature for automatic generation of multiple delivery orders, one for each product in the sale order line. In cases where the same product is listed on multiple lines, a single delivery order will be created, combining the total quantity of that product. 
### Key Features:
- The system produces delivery orders corresponding to the count of order lines in the sale order- Automatically links stock picking records to the corresponding sale order during the confirmation of a sale order.
- For products listed on multiple lines, a delivery order will be generated with the sum of the quantities for that specific product
- A smart button is activated on the sale order form to provide access to the linked delivery orders.

## Installation

1. **Clone or download the module**:

2. **Place the module in your Odoo addons folder**:
3. **Update the module list**:
- Go to Odoo **Apps** menu.
- Click on the **Update Apps List**.

4. **Install the module**:
- Find the module by searching for **SO Multiple DO** in the Apps menu.
- Click **Install**.

## Usage

1. Navigate to the **Sales** module and create a new sale order.
2. Confirm the sale order. A corresponding stock pickings (delivery order) will be created automatically based on the order line.
3. Access the smart button with the **truck icon** on the sale order, or visit the **Inventory** module to view the created delivery orders.