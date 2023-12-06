# API Specification

## 1. User Searching for Thrift Stores

The API calls are made in this sequence when a user visits the website for thrift stores:

### 1.1 Get Stores - `/stores/` (GET)

Retrieves the catalog of thrift stores in website.

**Returns**:

```json
{
  "name": "string",
  "rating": "integer",
  "address": "string",
  "type": "string"
}
```

### 1.2 Get Store By ID - '/stores/{id}' (GET)

Retrieves the thrift store by ID.

**Returns**:

```json
{
  "name": "string",
  "rating": "integer",
  "address": "string",
  "type": "string"
}
```

### 1.3 Create a Store - '/stores/{store_id}' (POST)

Creates a thrift store.

**Returns**:

```
"OK"
```

### 1.4 Update Store - '/stores/{store_id}' (PUT)

Updates the name, address, or type of a specific store
attribute must be either "name", "address", "type"

**Request**:

```json
{
  "attribute": "string",
  "new_attribute": "string"
}
```

**Returns**:

```
"OK"
```

## 2. User Review

The API calls are made in this sequence when a user interacts with reviews for a thrift store:

### 2.1 View a Store's reviews - `/reviews/{store_id}` (GET)

A call to retrieve the list of reviews for a store.

**Returns**:

```json
{
"name": "string" /* Account Name */
"rating": "float" /* Between 0 and 5 */
"review": "string" /* User review of thrift store */
}
```

### 2.2 Leave a review - `/reviews/create_review` (POST)

A call to create a new review for a thrift store.

**Request**:

```json
{
"rating": "integer" /* Between 0 and 5 */
"name": "string" /* Account Name */
"review": "string" /* User review of thrift store */
}
```

**Returns**:

```
"OK"
```

### 2.3 View the ranking and rank of specfic store - `/reviews/average/{store_id}` (GET)

A call to retrieve the average rating and rank of store based on rating

**Return**:

```json
{
"store_rank": "integer" /* Between 1 and 5 */
"name": "string" /* Account Name */
"average_rating": "float /* User review of thrift store */
}
```

### 2.4 View a specific review - `/reviews/rating/{id}` (GET)

A call to retrieve a review for a thrift store.

**Return**:

```json
{
"rating": "integer" /* Between 1 and 5 */
"name": "string" /* Account Name */
"review": "string" /* User review of thrift store */
}
```

### 2.5 Reply to a review - `/reviews/{store_id}/{review_id}` (POST)

A call to create a reply comment to review for a thrift store.

**Request**:

```json
{
"rating": "integer" /* Between 1 and 5 */
"name": "string" /* Account Name */
"review": "string" /* User review of thrift store */
}
```

**Returns**:

```
"OK"
```

### 2.6 Sort Reviews - `/reviews/search/{store_id}` (GET)

Filter reviews

**Request**:

```json
{
"store_id": "integer"
"upper_rating": "integer" /* between 0 and 5 */
"lower_rating": "integer" /* between 0 and 5, <= upper_rating */
"customer_name": "string" /* optional sorting based on customer name */
"sort_order": "string" /* either asc or desc */
}
```

**Returns**:

```json
{
  "id": "integer",
  "account_name": "string",
  "rating": "integer",
  "description": "string"
}
```

### 2.7 Update Review - `/reviews/update/{review_id}` (PUT)

Update an existing review

**Request**:

```json
{
"review_id": "integer"
"name": "string"
"rating": "integer"
"description": "string"
}
```

**Returns**:

```
  "OK"
```

## 4. Admin Functions

### 4.1 Reset Reviews - `/admin/reset/{store_id}` (DELETE)

A call to reset reviews will delete all reviews under a specific store

**Returns**:

```
"OK"
```

### 4.2 Reset - `/admin/reset/{store_id}` (DELETE)

A call to reset all reviews for a particular store

**Returns**:

```
"OK"
```

### 4.3 Reset Specific Review - `/admin/reset/{review_id}` (DELETE)

A call to reset specific review will delete one specific review

**Returns**:

```
"OK"
```
