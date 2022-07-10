# CCSupply

CCSupply is a supply and ownership data analysis tool for [Curio Cards](https://curio.cards). Unlike the vast majority of NFT projects, Curio Cards was created before the ERC721 standard was defined. Combined with the fact that many Ethereum wallets from that era were lost, it's difficult to know how many Curio Cards are in active circulation. This tool uses the Curio Cards subgraph and the Etherscan API to show how many Curio Cards have been burned, how many are in inactive (possibly lost) wallets, and how many remain in active circulation.

## Requirements

- Python
- [Pandas library for Python](https://pandas.pydata.org)
- [Requests library for Python](https://pypi.org/project/requests)
- [The Graph API key](https://thegraph.com/studio/apikeys/)
- [Etherscan API key](https://etherscan.io/myapikey)

Note: While the Etherscan API is completely free, The Graph is only free for the first 1000 API requests, after which it costs a small amount of GRT. As of July 2022, running CCSupply requires 128 API requests from The Graph, or ~1/8 of the free allowance.

## How To Use

- Download the repository
- In the same directory as CCSupply.py, create text files named "The_Graph_API_Key.txt" and "Etherscan_API_Key.txt". Save your corresponding API keys as a single line to each of these files.
- Run CCSupply.py using Python

Note: When run for the first time, CCSupply will create directories called "address_tx" and "cardBalances" to store API responses from Etherscan and The Graph, respectively. Please make sure you have at least 1 GB of free space available on your drive. The next time you run, CCSupply will detect these folders, and will ask you if you want to use the old data, or if you want to replace the old data by querying the APIs again.

## Outputs

- Card_Supply.csv: A summary of relevant stats for each Curio Card, including total supply, burned supply, inactive supply (# of cards in wallets with no OUT transactions in the last 1000 days), and the remaining active supply
- Card_Supply_Verbose.csv: A longer summary similar to Card_Supply.csv, but adding breakdowns by card wrapper (unwrapped, official wrapper, unofficial wrapper)
- Zombie_Addresses.txt: A list of all addresses that hold unwrapped Curio Cards but haven't executed an OUT transaction in over 1000 days (cards in these addresses are considered inactive)
- All_Holders.csv: A table of all addresses holding Curio Cards, as well as holdings broken down by card type and wrapper

## Future Work

CCSupply is currently a work in progress. Next steps are:
- Get user feedback on output format (Are current outputs useful, or are there other outputs that would be useful?)
- Get user feedback on usability (Does the software work as intended cross-platform? Are there changes that we could make to reduce dependencies and/or make it easier to use?)
- Online hosting (How can we provide a service that delivers outputs on a regular basis to the community? A Twitter or Discord bot, or a dedicated website? How often should new data be delivered?)

If you'd like to contribute, feel free to make a pull request, or join the discussion in the [Curio Discord](https://discord.curio.cards)
