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
6. **reviews**.py: put in line breaks on lines 28, 49, and 74
7. **database**.py: Having a separate file where the schemas are implemented makes it easier to find code. Better breaks up the code into more logical pieces.
8. Some of the API seems a little inconsistent in the sense of what falls under admin and what doesn't. Choose where store updating happens, either admin or stores, not both! The description looks like it should be in the stores endpoint, functionally.
9. Include all tables in as schemas, not just two, if you're gonna use schemas.
10. Need to create an endpoint to delete stores
11. Need to expose the reveiw_id when returning reviews so we know what to do.
12. The "stores/create_store" endpoint doesn't seem to be actually creating stores.
