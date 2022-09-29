# CSGO Rank Logger
A little Python thing to get the CSGO ranks of you and your friends and log them to a database.

## Requirements
- A second Steam account with CSGO that is friends with everyone you want to track
- A DynamoDB table in AWS
- AWS CLI set up on the computer you are running on with permissions to write to DynamoDB
- The Steam3 IDs of everyone you want to get the rank of (Use https://steamid.io/ to help you, you just need the numbers in the Steam3 ID)

## How to
1. Copy Config.py-example to Config.py
2. Enter your DynamoDB table name and region in Config.py
3. Enter your friends names and Steam3 IDs in Config.py
4. Run it and log in
