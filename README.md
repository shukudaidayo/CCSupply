# CCSupply

CCSupply is a supply and ownership data analysis tool and website for [Curio Cards](https://curio.cards). Unlike the vast majority of NFT projects, Curio Cards was created before the ERC721 standard was defined. Combined with the fact that many Ethereum wallets from that era were lost, it's difficult to know how many Curio Cards are in active circulation. This tool uses the Curio Cards subgraph and the Etherscan API to show how many Curio Cards have been burned, how many are in inactive (possibly lost) wallets, and how many remain in active circulation.

This project is hosted as a website at [ccsupply.xyz](https://ccsupply.xyz) with data updated weekly, however, if you'd like access to more current data or to host your own version of the website, this repository gives you the resources needed to do so.

## Requirements

- Python 3
- [Pandas library for Python](https://pandas.pydata.org)
- [Requests library for Python](https://pypi.org/project/requests)
- [The Graph API key](https://thegraph.com/studio/apikeys/)
- [Etherscan API key](https://etherscan.io/myapikey)

Note: While the Etherscan API is completely free, The Graph is only free for the first 1000 API requests, after which it costs a small amount of GRT. As of July 2022, running CCSupply requires 128 API requests from The Graph, or ~1/8 of the free allowance.

## Outputs

CCSupply.py generates the following outputs, saved to the same directory as CCSupply.py:
- Card_Supply.csv: A summary of relevant stats for each Curio Card, including total supply, burned supply, inactive supply (# of cards in wallets with no OUT transactions in the last 1000 days), and the remaining active supply
- Card_Supply_Verbose.csv: A longer summary similar to Card_Supply.csv, but adding breakdowns by card wrapper (unwrapped, official wrapper, unofficial wrapper)
- Zombie_Addresses.txt: A list of all addresses that hold unwrapped Curio Cards but haven't executed an OUT transaction in over 1000 days (cards in these addresses are considered inactive)
- All_Holders.csv: A table of all addresses holding Curio Cards, as well as holdings broken down by card type and wrapper

## How To Use

There are two ways to run CCSupply: as a standalone Python script, and as a website. Instructions on how to run both are presented below.

### Standalone Script

To run the Python script:
- Download the repository
- In the same directory as CCSupply.py, create text files named "The_Graph_API_Key.txt" and "Etherscan_API_Key.txt". Save your corresponding API keys as a single line to each of these files.
- Run CCSupply.py using Python 3
- Follow the terminal prompts

Note: When run for the first time, CCSupply will create directories called "address_tx" and "cardBalances" to store API responses from Etherscan and The Graph, respectively. Please make sure you have at least 1 GB of free space available on your drive. The next time you run, CCSupply will detect these folders, and will ask you if you want to use the old data, or if you want to replace the old data by querying the APIs again.

### Website

The website in this repository is currently hosted at [ccsupply.xyz](https://ccsupply.xyz). However, to host this site on your own:
- Download the repository
- Save index.html, favicon.ico, and the src folder to the hosted folder (e.g. public_html), and create a folder named 'data'
- In an unhosted folder, save CCSupply.py
- Run CCSupply.py with Python 3 and follow the terminal prompts. This will create address_tx and cardBalances directories
- Set up a weekly cron job that runs CCSupply.py, supplying the necessary terminal inputs, copies the output files to the hosted 'data' folder, and compresses them into All_Files.zip. For example, the cron job can run a bash script like:

```
cd /path/to/unhosted/directory
echo -e 'n/ny' | python3 CCSupply.py && cp Card_Supply.csv Card_Supply_Verbose.csv Zombie_Addresses.txt All_Holders.csv /path/to/hosted/directory/data
cd /path/to/hosted/directory/data
zip All_Filed.zip *
```

Note: Shared hosting services may not have Python 3 or the necessary Python libraries installed. In that case, a VPS may be required to run CCSupply.py on the server.

## Future Work

CCSupply remains under development. Next steps are:
- Get user feedback on output format (Are current outputs useful, or are there other outputs that would be useful?)
- Get user feedback on usability (Does the software work as intended cross-platform? Are there changes that we could make to reduce dependencies and/or make it easier to use?)
- Get user feedback on website UX/UI (Is the site broken on certain browsers/devices? What changes could make the site more user-friendly?
- Other online hosting (Can/should we provide other services that deliver outputs on a regular basis to the community, such as a Twitter or Discord bot?)

If you'd like to contribute, feel free to make a pull request, or join the discussion in the [Curio Discord](https://discord.curio.cards)
