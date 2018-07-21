# restaurantAPI
Django project allowing basic rest endpoints for taking and managing orders for a restaurant.

Assumptions:
- Customers are users that are not staff members
- Kitchen staff are users that are marked as staff members but not super users
- Managers are marked as both staff members and super users.

Validation:
Currently there is no validation on the request endpoints other than enquiring on the user making the request.
Orders being created will only be populated with the 'table_number' and 'menu_items' fields
Orders being updated will only have the 'order_complete' field updated.
Orders being deleted will be deleted providing a record is found.

Database:
A Postgres database was used for this for two reasons:
- nplan are planning on using postgres as a database in future so I thought it would be a good time to get some experience in it.
- postgres can store arrays of data in fields which allows for storing multiple menu items in one order row without having to create a linked table in the db.

API Endpoints:
  - Create Order:
 http://127.0.0.1:8000/order/createorder/
 * Allows a user to add a new order via a post request. 
 * User must not be a staff member.
 * While no fields are validated, only the table number and menu item fields will ever be populated in the database based of the passed in request.
 
 Example create order request:
 {
    "table_number": 84,
    "menu_items":[12, 6, 94] 
 }
 
 - Manage order:
 http://127.0.0.1:8000/order/manageorder/pk
 * The order id must be passed in instead of 'pk' in the http request.
 * Allows both kitchen staff and managers to make put requests to mark an order as complete
 * Allows any user to view an order via a get request
 * Allows only managers (super-users) to delete orders via delete requests
 
 Example update request:
 http://127.0.0.1:8000/order/manageorder/3
 { "order_complete":true}

 
