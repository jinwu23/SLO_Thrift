# Fake Data Modeling
link to python file- [link](https://github.com/jinwu23/SLO_Thrift/blob/main/src/populate_posts.py)  

With this file we ended up with 1,101,000 rows of data in our database.  
We have 1,000 rows for each specific store in our database as that felt like a good amount due to this being a SLO area thrift store database.  
For each store, we have 100 reviews, we thought that would be a good representation of how many people would leave a review on a store.  
For each review, we have 10 replies, we thought that replies would be less common than reviews but still enough for a discussion.  

# Performance results of hitting endpoints
### 1.1 Get Stores - `/stores/` (GET)  
('Execution Time: 37.007 ms',)  
### 1.2 Get Store By ID - '/stores/{id}' (GET)  
('Execution Time: 16.084 ms',)  
### 1.3 Create a Store - '/stores/{store_id}' (POST)  
('Execution Time: 0.188 ms',)
### 1.4 Update Store - '/stores/{store_id}' (PUT)
('Execution Time: 0.248 ms',)
### 2.1 View a Store's reviews - `/reviews/{store_id}` (GET)
('Execution Time: 17.689 ms',)
### 2.2 Leave a review - `/reviews/review/{store_id}` (POST)
('Execution Time: 0.531 ms',)
### 2.3 View the ranking and rank of specfic store - `/reviews/average/{store_id}` (GET)
('Execution Time: 37.839 ms',)
### 2.4 View a specific review - `/reviews/rating/{id}` (GET)
('Execution Time: 0.122 ms',)
### 2.5 Reply to a review - `/reviews/{store_id}/{review_id}` (POST)
('Execution Time: 0.569 ms',)
### 2.6 Sort Reviews - `/reviews/search/{store_id}` (GET)
('Execution Time: 27.376 ms',)
### 2.7 Update Review - `/reviews/update/{review_id}` (POST)
('Execution Time: 0.174 ms',)
### 4.1 Reset Reviews - `/admin/reset/{store_id}` (POST)
('Execution Time: 9025.089 ms',)
### 4.2 Reset Specific Review - `/admin/reset/{review_id}` (POST)
('Execution Time: 9220.603 ms',)
### 4.3 Update Descriptions - `/admin/update/description/{store_id}` (POST)
('Execution Time: 0.208 ms',)

## 3 slowest endpoints
### 2.3 View the ranking and rank of specfic store - `/reviews/average/{store_id}` (GET)
### 4.1 Reset Reviews - `/admin/reset/{store_id}` (POST)
### 4.2 Reset Specific Review - `/admin/reset/{review_id}` (POST)

# Performance tuning
### 2.3 View the ranking and rank of specfic store - `/reviews/average/{store_id}` (GET)
`('Subquery Scan on rankedaverage  (cost=4624.22..4658.90 rows=5 width=57) (actual time=37.561..37.782 rows=1 loops=1)',)
('  Filter: (rankedaverage.sid = 231)',)
('  Rows Removed by Filter: 999',)
('  ->  WindowAgg  (cost=4624.22..4645.56 rows=1067 width=65) (actual time=37.189..37.742 rows=1000 loops=1)',)
('        ->  Sort  (cost=4624.22..4626.89 rows=1067 width=57) (actual time=37.184..37.234 rows=1000 loops=1)',)
("              Sort Key: (COALESCE(round(avg(reviews.rating), 2), '0'::numeric)) DESC",)
('              Sort Method: quicksort  Memory: 100kB',)
('              ->  HashAggregate  (cost=4554.55..4570.56 rows=1067 width=57) (actual time=36.712..37.014 rows=1000 loops=1)',)
('                    Group Key: stores.id',)
('                    Batches: 1  Memory Usage: 321kB',)
('                    ->  Hash Join  (cost=40.01..4054.55 rows=100000 width=27) (actual time=0.281..25.456 rows=100000 loops=1)',)
('                          Hash Cond: (reviews.store_id = stores.id)',)        
('                          ->  Seq Scan on reviews  (cost=0.00..3751.00 rows=100000 width=10) (actual time=0.004..7.802 rows=100000 loops=1)',)
('                          ->  Hash  (cost=26.67..26.67 rows=1067 width=25) (actual time=0.273..0.274 rows=1004 loops=1)',)
('                                Buckets: 2048  Batches: 1  Memory Usage: 76kB',)
('                                ->  Seq Scan on stores  (cost=0.00..26.67 rows=1067 width=25) (actual time=0.003..0.171 rows=1004 loops=1)',)
('Planning Time: 0.612 ms',)
('Execution Time: 37.839 ms',)`  

This explain to me meant that the db was getting the average rating of every store, assigning it a rank, and then doing a sequential scan on the stores via name to get the data of the store I wanted. I added an index on the stores table on name to speed up the query.
    
    create index store_name_idx on stores(name)  
    
`('Subquery Scan on rankedaverage  (cost=4614.74..4647.33 rows=5 width=57) (actual time=31.927..32.239 rows=1 loops=1)',)
('  Filter: (rankedaverage.sid = 433)',)
('  Rows Removed by Filter: 993',)
('  ->  WindowAgg  (cost=4614.74..4634.80 rows=1003 width=65) (actual time=31.728..32.203 rows=994 loops=1)',)
('        ->  Sort  (cost=4614.74..4617.24 rows=1003 width=57) (actual time=31.723..31.749 rows=994 loops=1)',)
("              Sort Key: (COALESCE(round(avg(reviews.rating), 2), '0'::numeric)) DESC",)
('              Sort Method: quicksort  Memory: 99kB',)
('              ->  HashAggregate  (cost=4549.69..4564.74 rows=1003 width=57) (actual time=31.298..31.574 rows=994 loops=1)',)
('                    Group Key: stores.id',)
('                    Batches: 1  Memory Usage: 321kB',)
('                    ->  Hash Join  (cost=38.57..4050.68 rows=99802 width=27) (actual time=0.185..20.345 rows=99402 loops=1)',)
('                          Hash Cond: (reviews.store_id = stores.id)',)
('                          ->  Seq Scan on reviews  (cost=0.00..3749.02 rows=99802 width=10) (actual time=0.004..4.494 rows=99402 loops=1)',)
('                          ->  Hash  (cost=26.03..26.03 rows=1003 width=25) (actual time=0.176..0.177 rows=1002 loops=1)',)
('                                Buckets: 1024  Batches: 1  Memory Usage: 68kB',)
('                                ->  Seq Scan on stores  (cost=0.00..26.03 rows=1003 width=25) (actual time=0.003..0.093 rows=1002 loops=1)',)
('Planning Time: 0.206 ms',)
('Execution Time: 32.287 ms',)`

### 4.1 Reset Reviews - `/admin/reset/{store_id}` (POST)
`('Delete on stores  (cost=0.28..8.29 rows=0 width=0) (actual time=0.146..0.146 rows=0 loops=1)',)
('  ->  Index Scan using stores_pkey on stores  (cost=0.28..8.29 rows=1 width=6) (actual time=0.119..0.119 rows=1 loops=1)',)
('        Index Cond: (id = 999)',)
('Planning Time: 0.349 ms',)
('Trigger for constraint reviews_store_id_fkey on stores: time=64.994 calls=1',)
('Trigger for constraint replies_review_id_fkey on reviews: time=8959.841 calls=100',)
('Execution Time: 9025.089 ms',)`  

This explain to me meant that the db had to drop each review and reply to the review which had foreign key references to the particular store but was doing a sequential scan on those drops to find the reviews and replies with references to the dropped store
    
    create index store_id_idx on reviews(store_id)  
    create index store_id_idx on replies(review_id)  

`('Delete on stores  (cost=0.28..8.29 rows=0 width=0) (actual time=0.033..0.033 rows=0 loops=1)',)
('  ->  Index Scan using stores_pkey on stores  (cost=0.28..8.29 rows=1 width=6) (actual time=0.007..0.007 rows=1 loops=1)',)
('        Index Cond: (id = 765)',)
('Planning Time: 0.120 ms',)
('Trigger for constraint reviews_store_id_fkey on stores: time=0.181 calls=1',)
('Trigger for constraint replies_review_id_fkey on reviews: time=1.010 calls=100',)
('Execution Time: 1.255 ms',)`

### 4.2 Reset Specific Review - `/admin/reset/{review_id}` (POST)
`('Delete on reviews  (cost=0.00..4001.00 rows=0 width=0) (actual time=17.793..17.794 rows=0 loops=1)',)
('  ->  Seq Scan on reviews  (cost=0.00..4001.00 rows=100 width=6) (actual time=0.336..17.652 rows=100 loops=1)',)
('        Filter: (store_id = 22)',)
('        Rows Removed by Filter: 99802',)
('Planning Time: 0.204 ms',)
('Trigger for constraint replies_review_id_fkey: time=9202.667 calls=100',)
('Execution Time: 9220.603 ms',)`  

This explain to me meant that the db had to drop each review and reply to the review which had foreign key references to the particular store but was doing a sequential scan on those drops to find the reviews and replies with references to the dropped store
    
    create index store_id_idx on reviews(store_id)  
    create index store_id_idx on replies(review_id)  

`('Delete on reviews  (cost=0.29..12.76 rows=0 width=0) (actual time=0.120..0.120 rows=0 loops=1)',)
('  ->  Index Scan using store_id_idx on reviews  (cost=0.29..12.76 rows=99 width=6) (actual time=0.014..0.025 rows=100 loops=1)',)
('        Index Cond: (store_id = 987)',)
('Planning Time: 0.036 ms',)
('Trigger for constraint replies_review_id_fkey: time=0.981 calls=100',)
('Execution Time: 1.117 ms',)`
