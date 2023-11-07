# Example workflow 1

Jin is an avid user of SLO Thrift.  
One day he realizes that the type of a particular thrift store is not up to date with its current inventory.  
First, Jin requests to see all the thrift stores on the website by calling GET /stores.  
Jin sees that a particular store has the wrong type of goods.  
Jin then initiates a request to update the store description.  
To do so he calls POST /stores/update_type/{store_id} and passes in the correct type of the store.  
The description then changes and Jin is happy :)

# Testing GET /stores

curl -X 'POST' \  
 'https://slo-thrift3.onrender.com/stores/update_type/1?new_type=clothing%2C%20furniture%2C%20books%2C%20electronics%2C%20antiques%2C%20etc' \  
 -H 'accept: application/json' \  
 -H 'access_token: slo-thrift-key' \  
 -d ''

Response: [
{
"id": 1,
"name": "Goodwill",
"rating": 3.1666666666666665,
"address": "880 Industrial Way San Luis Obispo, CA 93401",
"type": "it so mid"
},
{
"id": 2,
"name": "Fred and Betty's Thrift Store",
"rating": 3,
"address": "532 Higuera St, San Luis Obispo, CA 93401",
"type": "clothing"
}
]

# Testing POST /stores/update_type/{store_id}

curl -X 'POST' \
 'http://127.0.0.1:3000/stores/update_type/1?new_type=gadgets' \
 -H 'accept: application/json' \
 -H 'access_token: slo-thrift-key' \
 -d ''

Response: "OK"

# Example workflow 2

Tom is a frequent customer of Goodwill and loves their store, however, he has moved to a new area, looking for his favorite thrift store.
Hoping to go on a thrifting session, he looks for nearby stores by calling GET /stores and viewing Goodwill stores nearby.
He decides that he wants to visit the one with the best ratings, and visits the ratings page by calling GET /reviews/{store_id}, showing the overall rating and reviews.
He leaves to go thrift and has an amazing experience, and feels the need to combat some of the poor ratings the store received.
He begins to write his own review by calling POST /reviews/create_review and describing his positive experience. He is ecstatic about the potential impact of his review!

# Testing GET /stores

curl -X 'POST' \  
 'https://slo-thrift3.onrender.com/stores/update_type/1?new_type=clothing%2C%20furniture%2C%20books%2C%20electronics%2C%20antiques%2C%20etc' \  
 -H 'accept: application/json' \  
 -H 'access_token: slo-thrift-key' \  
 -d ''

Response: [
{
"id": 1,
"name": "Goodwill",
"rating": 3.1666666666666665,
"address": "880 Industrial Way San Luis Obispo, CA 93401",
"type": "it so mid"
},
{
"id": 2,
"name": "Fred and Betty's Thrift Store",
"rating": 3,
"address": "532 Higuera St, San Luis Obispo, CA 93401",
"type": "clothing"
}
]

# Testing GET /reviews/{store_id}

curl -X 'GET' \
 'http://127.0.0.1:3000/reviews/1' \
 -H 'accept: application/json' \
 -H 'access_token: slo-thrift-key'

Response: [
{
"account": "ian",
"rating": 5,
"description": "meh"
},
{
"account": "gabriel",
"rating": 1,
"description": "trash"
},
{
"account": "johnny",
"rating": 1,
"description": "this place sucks!"
},
{
"account": "Ivan",
"rating": 5,
"description": "Massive and Busy!"
},
{
"account": "ivan",
"rating": 2,
"description": "no"
},
{
"account": "Ivan",
"rating": 5,
"description": "Amazing!"
}
]

# Testing POST /reviews/create_review

curl -X 'POST' \
 'http://127.0.0.1:3000/reviews/create_review?store_id=1' \
 -H 'accept: application/json' \
 -H 'access_token: slo-thrift-key' \
 -H 'Content-Type: application/json' \
 -d '{
"name": "Tom",
"rating": 5,
"description": "Such an amazing thrift shop"
}'

Response: "OK"

# Example Workflow 3

Annie is an active community member of SLO Thrift and an owner of a thift store.
She likes to look at and respond to specific reviews that her customers leave.
Annie wanted to respond to the review that her friend Jeremiah left by calling GET /reviews/{id} to view the specific review that he left.
She is thankful for the kind comments that Jeremiah left behind so she decides to thank him in response.
She does this by calling POST /reviews/{id} in order to reply to Jeremiah's review.
Annie can now see her response pop up alongside Jeremiah's review, and she is delighted that she could thank her friend for the positive feedback.

# Testing GET /reviews/{id}

curl -X 'GET' \
 'http://127.0.0.1:3000/reviews/rating/19' \
 -H 'accept: application/json' \
 -H 'access_token: slo-thrift-key'

Response: {
"account": "Jeremiah",
"rating": 5,
"description": "Annie's shop is so amazing"
}

# Testing POST /reviews/{id}

curl -X 'POST' \
 'http://127.0.0.1:3000/reviews/19' \
 -H 'accept: application/json' \
 -H 'access_token: slo-thrift-key' \
 -H 'Content-Type: application/json' \
 -d '{
"name": "Annie",
"description": "Thank you so much Jeremiah!"
}'

Response: "OK"

# Example Workflow 4

John only goes to one thrift store due to undying loyalty.
One day he decided to check out how the store is doing on SLO_Thrift by calling GET /stores.
John sees that his store "Tremendous Thrift" does not exist in the database!
He is immensely devastated but he finds out that he can add the store himself!
John calls POST /store/create_store and passes it a dictionary with name, rating, address, type.
John is happy that his store is now in the database :)

# Testing GET /stores

curl -X 'POST' \  
 'https://slo-thrift3.onrender.com/stores/update_type/1?new_type=clothing%2C%20furniture%2C%20books%2C%20electronics%2C%20antiques%2C%20etc' \  
 -H 'accept: application/json' \  
 -H 'access_token: slo-thrift-key' \  
 -d ''

Response: [
{
"id": 1,
"name": "Goodwill",
"address": "880 Industrial Way San Luis Obispo, CA 93401",
"type": "gadgets",
"rating": 3.4285714285714284
},
{
"id": 2,
"name": "Fred and Betty's Thrift Store",
"rating": 3,
"address": "532 Higuera St, San Luis Obispo, CA 93401",
"type": "clothing"
}
]

# Testing POST /store/create_store

curl -X 'POST' \
 'http://127.0.0.1:3000/stores/create_store' \
 -H 'accept: application/json' \
 -H 'access_token: slo-thrift-key' \
 -H 'Content-Type: application/json' \
 -d '{
"name": "Tremendous Thrift",
"address": "1 Grand Ave",
"type": "Clothes and Furniture"
}'

Response: "OK"
