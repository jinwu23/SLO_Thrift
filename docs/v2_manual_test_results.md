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
