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
