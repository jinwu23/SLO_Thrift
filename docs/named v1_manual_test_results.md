# Example workflow
John only goes to one thrift store due to undying loyalty. 

One day he decided to check out how the store is doing on SLO_Thrift by calling GET /stores.

John sees that his store "Tremendous Thrift" does not exist in the database! He is immensely devastated but he finds out that he can add the store himself! 

John calls POST /store/create_store and passes it a dictionary with name, rating, address, type. 

John is happy that his store is now in the database :)

# Testing results
<Repeated for each step of the workflow>
1. curl -X 'POST' \'https://slo-thrift3.onrender.com/store/create_store' \-H 'accept: application/json' \-H 'access_token: slo-thrift-key' \-H 'Content-Type: application/json' \-d 
	'{"name": "Fred and Betty'''s Thrift Store","rating": 5,"address": "532 Higuera St, San Luis Obispo, CA 93401","type": "clothing"}'
 
2."OK"
