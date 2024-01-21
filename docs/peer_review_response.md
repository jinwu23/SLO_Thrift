### Peer Review Response Joe Simopoulos

# Code Review Comments:

1. **server**.py: Get rid of unnecessary, commented-out routes.
   deleted commented out routes.
2. **server**.py: We don't need the CORS middleware, unnecessary
   dependency.
   deleted unused dependency
3. **API files**: Be consistent with the function declaration comments. Admin file function comments include return values, the others do not.
   Got rid of function comments including return values in admin.py for consistency.
4. **stores**.py: The SQL queries on the "/" and "/{id}" endpoints are way too long, break them up and make them readable.
   Broke down endpoints "/" and "/{id}" in stores.py
5. **auth**.py: Again, strip down the unnecessary things. The demo key isn't necessary and just confusing when looking at the point of auth.py. (I know you probably got this from him, but I'm having hard time finding things wrong with your code!)
   Didn't do anything with this because it was part of code from Professor
6. **reviews**.py: put in line breaks on lines 28, 49, and 74
   Added line breaks
7. **database**.py: Having a separate file where the schemas are implemented makes it easier to find code. Better breaks up the code into more logical pieces.
   we have a schema.sql file
8. Some of the API seems a little inconsistent in the sense of what falls under admin and what doesn't. Choose where store updating happens, either admin or stores, not both! The description looks like it should be in the stores endpoint, functionally.
   Admins are allowed to do certain types of updates whereas general users are not.
9. Include all tables in as schemas, not just two, if you're gonna use schemas.
   Included all tables
10. Need to create an endpoint to delete stores
    Created endpoint to delete stores in admin.py
11. Need to expose the reveiw_id when returning reviews so we know what to do.
    Exposed id when inserting reviews
12. The "stores/create_store" endpoint doesn't seem to be actually creating stores.
    It is creating stores

# Test Results Comments

CURRENTLY EDITING:

Run Throughs: Right off the bat, the /stores endpoint is not returning anything! My curl is not at least. Not sure if I am calling wrong (I see a "tags" list in the api router), but I can get specific stores by putting a store id after.

Now the "/stores" endpoint is just returning just one value.

The other endpoints seem to be working well, including both the posts and gets!!

Ian - Store endpoint working on my end.

MY TESTS:

1.) NEW THRIFT STORE ON THE BLOCK WITH TWO GOALS: Exploit the free market and sabotage.

My Mom's Shop and Pop (like the pistol) is entering the SLO thrift arena with one thing on their mind: sabotage. With this fancy new app, they are going to sign up and write terrible reviews about other shops under the alias "Big Hundos" and write good reviews for their own shop.

They start by calling /stores/create_store
They then write terrible reviews for the other shops at the /reviews/create_review endpoint.
They then write good reviews for their shop under the same endpoint.

**_TEST_**
Create Store:
Not successful! (Unless someone deleted it) I was returned "OK" but could not find my store
Ian - fixed this problem, I had to create a initializer entry for the review so that there is a value to be read
from the review table when trying to calculate average rating.

```
curl --location 'https://slo-thrift3.onrender.com/stores/create_store' \
--header 'access_token: slo-thrift-key' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Mom'\''s Shop and Pop",
    "rating": 6,
    "address": "666 Palm Street",
    "type": "Only the best"
}'
```

Good Review:
Could not perform a good review because the store wasn't created.
Ian - problem should be fixed, store was being created but it wasn't available to be read due to how average rating
is calculated.

2.) Just had a horrendous experience at the new thrift store. Gotta let them know. (Didn't actually have a bad experience, just wanted other people to think so.

Bad Review:
Succssful!

```
curl --location 'https://slo-thrift3.onrender.com/reviews/create_review?store_id=1' \
--header 'access_token: slo-thrift-key' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Mom'\''s Shop and Pop",
    "rating": -1,
    "description": "This place was sub-par. Customer Service was like the slug from Monster'\''s Inc."
}'
```

3.) The admin heard about the experience and they're officially off the service!

**CAN'T ACTUALLY DO THIS BECAUSE THE STORE WASN'T CREATED BUT WILL DO MY BEST TO REENACT**
Ian - This works now
Takes a look at the store's reviews (repeats for every store):
Successful!

```
curl --location --request GET 'https://slo-thrift3.onrender.com/reviews/1' \
--header 'access_token: slo-thrift-key' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Mom'\''s Shop and Pop",
    "rating": 5,
    "address": "666 Palm Street",
    "type": "Only the best"
}'
```

Deletes relevant posts ( I cannot look at the specific review Id without looking in the db so I won't actually run this command.) but this is what it would look like:

```
curl --location --request GET 'https://slo-thrift3.onrender.com/admin/reset/3' \
--header 'access_token: slo-thrift-key' \
--header 'Content-Type: application/json' \
```

Delete Store (again would, but cannot because it doesn't exist):
OH WAIT THEY CAN'T BECAUSE ITS IMPOSSIBLE TO DELETE STORES. Mom's Shop and Pop will cause havoc forever!
Ian - delete store endpoint has been created


### Peer Review Response Nicholas Hotelling

# Code Review Comments:

1. reveiws.py - change "/reveiws/create_review" endpoint to a post to "/reveiws/{store_id}" This follows good practices more clearly.

   **Refactored create_review to /reviews/{store_id}**

2. reveiws.py - add comments to each endpoint describing what the inputs, outputs, and effects are (reply reveiw has no comments)
   
   **Added comments to endpoints**
   
3. stores.py - line 26: make querys be multiple lines for clarity! this is absurdly long.

   **Long queries broken up**

4. stores.py - get stores endpoint: instead of the for loop, use list comprehension  
  
   **Implemented List comprehension for endpoint**

5. stores.py - line 46: make query multiple lines for clarity!  

   **Made query more clear** 

6. stores.py - line 74: make the parameter binding dictionary multiple lines for clear reading  

   **Made dictionaries multiple lines**

7. stores.py - update_name: should be a put not a post.  

   **updated name**

8. stores.py -update_address: should be a put not a post.  

   **updated name**

9. stores.py - update_type: should be a put not a post.  

   **updated name**

10. stores.py - update_name, update_address, update_type should all be one put endpoint at "/stores/{store_id}", where body defines the changes  

    **combined all endpoints into one: put/stores/{store_id}**

11. stores.py - line 26: if a store has no reviews, it will not be shown. This is because the join from stores on reveiws will remove any stores with no reveiws.  

    **Changed join to left join** 

12. stores.py - line 46: again, stores with no reveiws will not appear  

    **Changed join to left join**

# Schema/API Design Comments:

1. stores: at least name, and possibly address and type, should not be nullable

   **I think we only want physical stores, so we will keep the requirements**

2. reveiws: account name should not be nullable
   
   **Changed to non nullable**
   
3. reveiws: store should not be nullable

   **Changed to non nullable**

4. reveiws: rating should not be nullable, and you could use a smaller int size for star based ratings
  
   **Changed to non nullable, int2 size**

5. reveiws: rating should have a constraint: (1-5, 1-10, 1-100, etc)

   **Added constraints (0-5)** 

6. replies: reveiw, name, and description should not be nullable

   **Changed to non nullable**

7. api_spec: 1.3 (create store) should not require an id. id should be generated and returned by the system  

   **id is not returned by system**

8. api_spec 1.4, 1.5, 1.6 should all be one PUT endpoint where changes go in the body: PUT: "/stores/{store_id}"

   **updated endpoints to a single one**

9. api_spec 2.1/2.2: rating types are inconsistent, and they are inconsistent with the schema as well. is it an integer or a float?? 

   **rating types are inconsistent because one is a user input of rating which must be between 0-5 and one is a calculated rating from database as an average so it is a float**

10. api_spec: 2.3: creating a review should return the id of the reveiw 

    **now returns id of review**

11. general concern: following good practices, it makes sense to have most of the reveiws endpoints be a subset of /stores. example (PUT "/stores/{store_id}/reveiws" to create a reveiw for a store, GET "/stores/{store_id}/reveiws" to get all reveiws for a store)

    **consolidated endpoints** 

12. api_spec 2.2/2.3: no way for the user to tell the system which store they are interacting with.  

    **2.2 asks for store_id**

### Peer Review Response Maxwell Silver
1. /create_store should return the new store_id instead of http 200 "OK". **Fixed**

2. Standardize your returns. Create endpoints should all return the new id and updates should all return "OK".**Fixed**

3. Validation in your endpoints to check for required SQL fields. **Fixed**

4. Have separate return statements inside and outside of your with clause, so in case transaction fails you can return http 400. **Added Test cases for failing transactions**

5. Improve error handling overall. For some of your endpoints, the user cannot tell if there are just no records in the db, or if there was an error.**Fixed**

6. Use ORM to make queries more readable and extensible.**Easier to understand SQL statements, but we structured them more clearly.**

7. Add logging to more easily diagnose bugs.

8. Add docstring to POST /reviews/{id}**Added docstrings**

9. Add some form of unit or integration testing to your project. **Not Code Review, more of suggestion, but will work on it.**

10. Use linting and max line length to ensure readability.**Adjusted line lengths**

11. You set up the ORM tables in database.py but it is never used. **Will get rid of if not used.**

12. /admin should have a different permission level than the rest of your APIs because of its delete capabilities. Right now they all depend upon the same api key.


Stores
1. For stores, do not let name, address, and type be nullable fields. **updated**

2. A unique constraint can be added to name to ensure that there aren't duplicate records for the same store.**stores can have same name, but I understand the duplicates.**

3. Depending on what you mean type to be, if it is only from a predefined set of values, you can use enum instead of text.**Want to leave open for any.**

Reviews
4. Don't let account_name, rating, and description be nullable.**Fixed**

5. Don't let a foreign key be nullable.**Fixed**

6. Rating doesn't have to be a bigint if it's going to be like a range of 1-5 or 1-10. **Fixed**

7. Set default values if appropriate. **Nothing should really have default value.**

Replies
8. Don't let review_id, account_name, and description be nullable.**Fixed**

9. Reviews are able to be deleted by DELETE /review/{review_id}, so consider adding cascading delete to your replies that reference the deleted review.

10. You can add a users or accounts table that contains account_name, so you can normalize your data.

API
11. You can add user auth and admin auth if you want there to be different permission levels within your app.

12. You could add a delete operation to be able to completely delete a store.
