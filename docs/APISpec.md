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

### 1.4 Update Store Name - '/stores/update_name/{store_id}' (POST)

Updates the name of specific store.

**Request**:

```json
{
  "name": "string"
}
```

**Returns**:

```
"OK"
```

### 1.5 Update Address - '/stores/update_address/{store_id}' (POST)

Updates the address of specific store.

**Request**:

```json
{
  "address": "string"
}
```

**Returns**:

```
"OK"
```

### 1.6 Update Type - '/stores/update_type/{store_id}' (POST)

Updates the type of specific store.

**Request**:

```json
{
  "type": "string"
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
"rating": "float" /* Between 1 and 5 */
"review": "string" /* User review of thrift store */
}
```

### 2.2 View a specific review - `/reviews/rating/{id}` (GET)

A call to retrieve a review for a thrift store.

**Return**:

```json
{
"rating": "integer" /* Between 1 and 5 */
"name": "string" /* Account Name */
"review": "string" /* User review of thrift store */
}
```

### 2.3 Leave a review - `/reviews/create_review` (POST)

A call to create a new review for a thrift store.

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

### 2.4 Reply to a review - `/reviews/{store_id}/{review_id}` (POST)

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

## 4. Admin Functions

### 4.1 Reset Reviews - `/admin/reset/{store_id}` (POST)

A call to reset reviews will delete all reviews under a specific store

**Returns**:

```
"OK"
```

### 4.2 Reset Specific Review - `/admin/reset/{review_id}` (POST)

A call to reset specific review will delete one specific review

**Returns**:

```
"OK"
```

### 4.3 Update Descriptions - `/admin/update/description/{store_id}` (POST)

A call to update descriptions for a store will add the admin description to database

**Request**:

```param
{
"descriptions": {description: "input"} /* dictionary of description to user input */
}
```

**Returns**:

```
"OK"
```
