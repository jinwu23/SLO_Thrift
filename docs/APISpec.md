# API Specification

## 1. User Searching for Thrift Stores
The API calls are made in this sequence when a user visits the website for thrift stores:

## 2. User Leaving Review 
The API calls are made in this sequence when a user leaves a review for a thrift store:

## 3. User Updating Store Descriptions
The API calls are made in this sequence when a user updates metadata about a store:
### 3.1 Update Descriptions - `/descriptions/update/{store_id}` (POST)
  A call to update descriptions for a store will add the user description to database
  
  **Request**:
  ```json
  {
  "descriptions" = {description: "input"} /* dictionary of description to user input */
  }
  ```
  **Returns**:
  ```json
  {
      "success": "boolean"
  }
  ```

## 4. Admin Functions 
### 4.1 Reset Reviews - `/admin/reset/{store_id}` (POST)
  A call to reset reviews will delete all reviews under a specific store
  
  **Returns**:
  ```json
  {
      "success": "boolean"
  }
  ```
