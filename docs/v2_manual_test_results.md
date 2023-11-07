# Example workflow
Jin is an avid user of SLO Thrift.  
One day he realizes that the type of a particular thrift store is not up to date with its current inventory.  
First, Jin requests to see all the thrift stores on the website by calling GET /stores.  
Jin sees that a particular store has the wrong type of goods.   
Jin then initiates a request to update the store description.   
To do so he calls POST /stores/update_type/{store_id} and passes in the correct type of the store.   
The description then changes and Jin is happy :)

# Testing results
<Repeated for each step of the workflow>
1. curl -X 'POST' \  
  'https://slo-thrift3.onrender.com/stores/update_type/1?new_type=clothing%2C%20furniture%2C%20books%2C%20electronics%2C%20antiques%2C%20etc' \  
  -H 'accept: application/json' \  
  -H 'access_token: slo-thrift-key' \  
  -d ''   
 
2."OK"

# Example workflow
Tom is a frequent customer of Goodwill and loves their store, however, he has moved to a new area, looking for his favorite thrift store. Hoping to go on a thrifting session, he looks for nearby stores by calling GET /stores and viewing Goodwill stores nearby. He decides that he wants to visit the one with the best ratings, and visits the ratings page by calling GET /reviews/{store_id}, showing the overall rating and reviews. He leaves to go thrift and has an amazing experience, and feels the need to combat some of the poor ratings the store received. He begins to write his own review by calling POST /reviews/{store_id}/ and describing his positive experience. He is ecstatic about the potential impact of his review!

# Testing results
<Repeated for each step of the workflow>
1. curl -X 'GET' \
  'https://slo-thrift3.onrender.com/stores/' \
  -H 'accept: application/json' \
  -H 'access_token: slo-thrift-key'
 
2.curl -X 'GET' \
  ''https://slo-thrift3.onrender.com/reviews/1' \
  -H 'accept: application/json' \
  -H 'access_token: slo-thrift-key'

3."OK"
