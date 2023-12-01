Concurrent Store Updates: update_store

Scenario:

Multiple clients attempt to update the details of the same thrift store simultaneously by calling the update_store endpoint with different attribute modifications.

Issue:

Without proper concurrency control, simultaneous updates can lead to a race condition where one update overwrites the changes made by another update, resulting in data inconsistency. LOST UPDATE

Consequence:

The final state of the thrift store may not reflect all the intended modifications, and some updates may be lost. This can lead to incorrect information being stored or displayed.

Solution:

Use READ COMMITTED isolation level to prevent dirty reads meaning that transactions will not see uncommitted changes made by other transactions. This helps in avoiding lost updates by ensuring that each transaction sees only committed changes.

![Screenshot 2023-11-28 233735](https://github.com/jinwu23/SLO_Thrift/assets/69867265/564ee13c-c4dc-45d2-82dd-048e9353fd19)

Concurrent Store Updates: Read Skew

Scenario:

Client 1 wants the data about a specific store (name, type). Client 2 visited the store and realized that the name and type of that address is wrong! Client two puts in a request to update the name and address of the store to be correct.

Issue:

Without proper concurrency control, Client 1 can get the name of the store before Client 2 updates both name and type. Client 1 then gets the type of the store and the type is the one Client 2 updated it with.

Consequence:

This gives Client 1 false data on what the store actually has.

Solution:

Use a singular select statement to get all data about a store at once so concurrent updates do not falsify data in the middle of selections.

![Screenshot 2023-11-28 233819](https://github.com/jinwu23/SLO_Thrift/assets/69867265/4e6996f3-c81c-4ed0-ac5f-793552fc134d)

Concurrent Store Updates: Non Repeatable Read

Scenario:

Client 1 wants to see the review with id 1. Client 2 just updated the review with id 1. Client 1 then checks the review again which returns a different rating from the one before

Issue:

Without proper concurrency control, Client 1 can get the rating before Client 2 manipulates the rating for the store. Client 1 then gets a different rating when they try to read the same rating.

Consequence:

This gives Client 1 inconsistencies in the data that they receive even though it's the same query

Solution:

Increase the isolation level to READ COMMIT and use FOR UPDATE to lock the rows before the update is commited

![Screenshot 2023-11-28 233940](https://github.com/jinwu23/SLO_Thrift/assets/97060375/582ea6f4-2f14-49b1-bc4e-7c2e55818864)
