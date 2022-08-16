#! /usr/bin/python

#CCSupply, a Curio Card supply and ownership data analysis tool by shukudaidayo
#Copyright (C) 2022 shukudaidayo

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or 
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#Import standard libraries
import json
import os
import random
import shutil
import sys
import time

#Import non-standard libraries
try:
    import pandas as pd
except ImportError:
    raise ImportError("You must install the pandas library from \
pandas.pydata.org before running this script")
try:
    import requests
except ImportError:
    raise ImportError("You must install the requests library from \
pypi.org/project/requests before running this script")

#Function to read API key from file
#Input is file name of text file containing the API key
#Returns contents of the text file
def get_api_key(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' not found, create a file named '%s' and write the \
API key to this file" % (filename, filename))
        sys.exit(1)

def try_cardBalances_query(api_url, query):
    i = 0
    while i < 3:
        try:
            response = requests.post(api_url, json={'query': query})
            data = json.loads(response.text)
            return response
        except JSONDecodeError:
            print("Error encountered, trying again...")
            i += 1
            time.sleep(5)
            pass
        print("Gave up cardBalances query.")
        f = open(filepath, 'w+')
        f.write(response.text)
        f.close()
        exit()

#Function to query Curio Cards subgraph for card balances for all 
#    holders' addresses
#Input is The Graph API key
#Returns nothing
#Saves all pages of subgraph response as json files in folder named 
#    "cardBalances"
def cardBalances_query(api_key):
    print("Querying Curio Cards subgraph...")
    api_url = "https://gateway.thegraph.com/api/" + api_key + \
                "/subgraphs/id/JBnWrv9pvBvSi2pUZzba3VweGBTde6s44QvsDABP47Gt"
    length = 0
    length_init = 0
    page = 0
    start_time = time.time()
    period = 15
    l_waiting_text = [
        "Chasing raccoons...",
        "Accessing Arctic World Archives...",
        "Picking apples...",
        "Mining Bitcoin...",
        "Crypto-Currency: Code is it!",
        "Looking for new alts to pump...",
        "Assembling party...",
        "Fusing art, technology, and science...",
        "We are all Marisol Vengas."
    ]
    while length >= length_init:
        query = """

        {
          cardBalances(first: 100, skip: """ + str(100*page) + """) {
            user {
              id
            }
            type {
              symbol
            }
            unwrapped
            wrappedOfficial
            wrappedUnofficial
          }
        }
        """
        response = try_cardBalances_query(api_url, query)
        data = json.loads(response.text)
        filepath = os.path.join("cardBalances", "cardBalances_" + str(page)
                + ".json")
        f = open(filepath, 'w+')
        f.write(response.text)
        f.close()
        length = len(data['data']['cardBalances'])
        if page == 0: length_init = length
        elapsed_time = time.time() - start_time
        if elapsed_time > period:
            print(random.choice(l_waiting_text))
            start_time = start_time + period
        page += 1
    print("Finished subgraph query")

#Function to download address transactions from Etherscan API
#Inputs are list of addresses to request and Etherscan API key
#Returns nothing
#Saves all API responses to folder named "address_tx"
#Only gets first page of results per address (latest 10000 transactions)
def address_query(l_id_to_check, d_tx_types, d_cs, api_key):
    print("Querying Etherscan API...")
    api_url = "https://api.etherscan.io/api"
    i = 0
    list_len = len(l_id_to_check)
    for address in l_id_to_check:
        #Progress bar
        sys.stdout.write('\r')
        j = round(i/(len(l_id_to_check)/29))
        sys.stdout.write("[%-29s] %s" % ('='*j, d_cs['Name'][j] +
                        " "*(14 - len(d_cs['Name'][j]))))
        sys.stdout.flush()
        #API query
        for key, action in d_tx_types.items():
            params = {"module": "account", "action": action, "address":
                    str(address), "sort": "desc", "apikey": api_key}
            response = requests.get(api_url, params=params)
            data = json.loads(response.text)
            filepath = os.path.join("address_tx", str(address)
                    + key + ".json")
            f = open(filepath, 'w+', encoding='utf-8')
            f.write(response.text)
            f.close
        i += 1
    print("\nFinished Etherscan query")

#Function to ask user whether or not to run API queries
#Input is question to be printed to console as string
#Returns bool (True = use existing data, False = run queries)
#Works with ask_yn_confirm to confirm user choice, 
#    loop back to ask_yn if unsure
def ask_yn(question):
    print(question)
    answer = input().lower().strip()
    while True:
        if (answer == "yes") or (answer == "y"):
            question2 = "Warning: Existing data may be out of date. \
Continue anyway? (Y/n)"
            return ask_yn_confirm(True, question, question2)
        elif (answer == "no") or (answer == "n"):
            question2 = "Warning: New subgraph query may result in GRT fees. \
Query anyway? (Y/n)"
            return ask_yn_confirm(False, question, question2)
        else:
            print("Please answer yes or no")
            answer = input().lower().strip()

#Function to confirm whether or not to run API queries with user
#Inputs are user response to ask_yn (bool), original question and 
#    confirmation question as strings
#Returns bool (True = use existing data, False = run queries) 
#    or loops back to ask_yn
def ask_yn_confirm(prev_answer, old_question, new_question):
    print(new_question)
    answer = input().lower().strip()
    while True:
        if (answer == "yes") or (answer == "y"):
            if prev_answer:
                return True
            else:
                return False
        elif (answer == "no") or (answer == "n"):
            return ask_yn(old_question)
        else:
            print("Please answer yes or no")
            answer = input().lower().strip()

#Function to ask user whether or not to run API queries (if existing
#    data not found)
#Input is question to be printed to console as string
#Exits program if user answers no
def ask_yn_exit(question):
    print(question)
    answer = input().lower().strip()
    while True:
        if (answer == "yes") or (answer == "y"):
            return
        elif (answer == "no") or (answer == "n"):
            print("Exiting...")
            sys.exit(1)
        else:
            print("Please answer yes or no")
            answer = input().lower().strip()

#Function to delete folder with error handling
def rm_folder(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))

#Function to prepare and execute subgraph query
#Inputs are bools that tell whether "cardBalances" and "address_tx"
#    folders exist
def query_subgraph(cbExists, zcExists):
    if cbExists: rm_folder("cardBalances")
    if zcExists: rm_folder("address_tx")
    graph_api_key = get_api_key("The_Graph_API_Key.txt")
    os.makedirs("cardBalances")
    cardBalances_query(graph_api_key)

#Check if address_tx and cardBalances folders exist
cbExists = os.path.exists("cardBalances")
zcExists = os.path.exists("address_tx")
if cbExists & zcExists:
    #Ask if new json query should be made
    question = "'cardBalances' and 'address_tx' directories found. \
Use existing data? (Y/n)"
    answer = ask_yn(question)
    if answer:
        #If yes, pass
        pass
    else:
        #If no, clear folder(s) and query subgraph
        query_subgraph(cbExists, zcExists)
else:
    #Ask to continue, clear folder(s), and query subgraph
    question = "'cardBalances' and/or 'address_tx' folder(s) not found. \
Run new query? Warning: May result in GRT fees (Y/n)"
    ask_yn_exit(question)
    query_subgraph(cbExists, zcExists)

#Read in all cardBalances json files and input into DataFrame df
page = 0
df = [""]
df_new = [""]
while page < len(os.listdir("cardBalances")):
    filepath = os.path.join("cardBalances", "cardBalances_" + str(page)
            + ".json")
    f = open(filepath, 'r')
    data = json.load(f)
    f.close
    if page == 0:
        df = pd.DataFrame(data["data"]["cardBalances"])
    else:
        df_new = pd.DataFrame(data["data"]["cardBalances"])
        df = pd.concat([df, df_new])
    page += 1

#Extract addresses and card symbols from tuples
df_all = pd.DataFrame(df['user'].tolist(), index=df.index)
df_temp = pd.DataFrame(df['type'].tolist(), index=df.index)

#Copy all data to DataFrame df_all
df_all['symbol'] = df_temp[['symbol']].copy()
df_all['unwrapped'] = df[['unwrapped']].copy()
df_all['wrappedOfficial'] = df[['wrappedOfficial']].copy()
df_all['wrappedUnofficial'] = df[['wrappedUnofficial']].copy()

#Re-type token counts to INT
df_all['unwrapped'] = pd.to_numeric(df_all['unwrapped'])
df_all['wrappedOfficial'] = pd.to_numeric(df_all['wrappedOfficial'])
df_all['wrappedUnofficial'] = pd.to_numeric(df_all['wrappedUnofficial'])

#Export all holders/holdings
f = open("All_Holders.csv", 'w+')
f.write(df_all.to_csv(index = False))
f.close

#Construct card supply DataFrame
d_cs = {'Serial': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, "17b"],
        'Name': ["Apples", "Nuts", "Berries", "Clay", "Paint", "Ink",
        "Sculpture", "Painting", "Book", "Future", "BTC Keys", "Mine Bitcoin",
        "BTC", "CryptoCurrency", "DigitalCash", "Original", "UASF",
        "To The Moon", "Dogs Trading", "MadBitcoins", "The Wizard",
        "The Bard", "The Barbarian", "Complexity", "Passion", "Education",
        "Blue", "Pink", "Yellow", "Eclipse", "UASFb"]}
df_cs = pd.DataFrame(data=d_cs)

#Define burn addresses
id_0000_burn = "0x0000000000000000000000000000000000000000"
id_dead_burn = "0x000000000000000000000000000000000000dead"
id_lc_burn = "0x77f84c36e451496d7f489efd16e9753fc2c8f0df"
id_timelock = "0x1b6a4a23df97a97feed5418b10db03ec63026aed"

#Add up token counts for each token and add to count lists
l_unwrapped = [0]*31
l_wrappedOfficial = [0]*31
l_wrappedUnofficial = [0]*31
l_lc_burn = [0]*31
l_dead_burnx = [0]*31
l_dead_burny = [0]*31
l_dead_burnz = [0]*31
i = 0
while i <= 30:
    symbol = "CRO" + str(df_cs.iat[i, 0])
    l_unwrapped[i] = df_all.loc[(df_all['id'] != id_0000_burn) &
                    (df_all['symbol'] == symbol), 'unwrapped'].sum()
    l_wrappedOfficial[i] = df_all.loc[df_all['symbol'] == symbol,
                        'wrappedOfficial'].sum()
    l_wrappedUnofficial[i] = df_all.loc[df_all['symbol'] == symbol,
                        'wrappedUnofficial'].sum()
    l_lc_burn[i] = df_all.loc[(df_all['id'] == id_lc_burn) &
                (df_all['symbol'] == symbol), 'unwrapped'].sum()
    l_dead_burnx[i] = df_all.loc[(df_all['id'] == id_dead_burn) &
                    (df_all['symbol'] == symbol), 'unwrapped'].sum()
    l_dead_burny[i] = df_all.loc[(df_all['id'] == id_dead_burn) &
                    (df_all['symbol'] == symbol), 'wrappedOfficial'].sum()
    l_dead_burnz[i] = df_all.loc[(df_all['id'] == id_dead_burn) &
                    (df_all['symbol'] == symbol), 'wrappedUnofficial'].sum()
    i += 1
l_supply = [sum(x) for x in zip(l_unwrapped, l_wrappedOfficial, 
        l_wrappedUnofficial)]
l_burned = [sum(x) for x in zip(l_dead_burnx, l_dead_burny, l_dead_burnz)]
l_inaccessible = [sum(x) for x in zip(l_lc_burn, l_burned)]
l_remain = [x - y for x, y in zip(l_supply, l_inaccessible)]

#Get total token supply by address
l_by_id = df_all['id'].unique().tolist()
i = 0
l_by_id_unwrapped = [0]*len(l_by_id)
l_by_id_wrappedOfficial = [0]*len(l_by_id)
l_by_id_wrappedUnofficial = [0]*len(l_by_id)
while i < len(l_by_id):
    l_by_id_unwrapped[i] = df_all.loc[df_all['id'] == l_by_id[i],
                            'unwrapped'].sum()
    l_by_id_wrappedOfficial[i] = df_all.loc[df_all['id'] == l_by_id[i],
                            'wrappedOfficial'].sum()
    l_by_id_wrappedUnofficial[i] = df_all.loc[df_all['id'] == l_by_id[i],
                            'wrappedUnofficial'].sum()
    i += 1
df_id_supply = pd.DataFrame()
df_id_supply['id'] = l_by_id
df_id_supply['unwrapped'] = l_by_id_unwrapped
df_id_supply['wrappedOfficial'] = l_by_id_wrappedOfficial
df_id_supply['wrappedUnofficial'] = l_by_id_wrappedUnofficial
df_id_supply = df_id_supply.set_index('id')

#Get list of ids to check if zombie (no outbound transactions in 1000 days)
#Only include addresses with unwrapped tokens, as wrappers are <1000 days old
#Exclude burn and timelock addresses, accounted for elsewhere
l_id_to_check = df_id_supply.loc[(df_id_supply['unwrapped'] != 0)
                 & (df_id_supply.index != id_0000_burn)
                 & (df_id_supply.index != id_dead_burn)
                 & (df_id_supply.index != id_lc_burn)
                 & (df_id_supply.index != id_timelock)].index.tolist()
d_tx_types = {
    "_tx": "txlist",
    "_tx_internal": "txlistinternal",
    "_tx_erc20": "tokentx",
    "_tx_erc721": "tokennfttx",
    "_tx_erc1155": "token1155tx",
    }
#Check if addresses_tx folder exists
zcExists = os.path.exists("address_tx")
if zcExists:
    #Use existing data
    pass
else:
    #Get API key, create folder, and query Etherscan
    escan_api_key = get_api_key("Etherscan_API_Key.txt")
    os.makedirs("address_tx")
    address_query(l_id_to_check, d_tx_types, d_cs, escan_api_key)

#Check for zombie addresses
#Only supports one json per address (up to 10000 transactions)
#If >=10k transactions, assumed active address
#If no transactions on Etherscan, assumed inactive address
l_isZombie = [True]*len(l_id_to_check)
currentTimestamp = int(time.time())
ageZombie = 1000*24*60*60
i = 0
while i < len(l_id_to_check):
    isZombie = True
    for key in d_tx_types.keys():
        filepath = os.path.join("address_tx", str(l_id_to_check[i])
                + key + ".json")
        f = open(filepath, "r", encoding='utf-8')
        transactions = json.load(f)
        df_trans = pd.DataFrame(transactions["result"])
        transactions_count = len(df_trans.index)
        #Iterate through transactions
        j = 0
        age = 0
        if transactions_count == 0:
            pass
        elif transactions_count >= 10000:
            isZombie = False
        else:
            while (j < transactions_count) & isZombie:
                #Check if transaction is outbound
                if df_trans["from"][j] == l_id_to_check[i]:
                    #Calculate age of transaction
                    blockTimestamp = int(df_trans["timeStamp"][j])
                    age = currentTimestamp - blockTimestamp
                    #Check if outbound transaction is younger than 1000 days
                    if age < ageZombie: isZombie = False
                j += 1
        f.close
    l_isZombie[i] = isZombie
    i += 1

#With zombie addresses identified, create list of zombie addresses
l_id_zombie = []
i = 0
while i < len(l_id_to_check):
    if l_isZombie[i]:
        l_id_zombie.append(l_id_to_check[i])
    i += 1

#Export zombie addresses
f = open("Zombie_Addresses.txt", 'w+')
for address in l_id_zombie:
    f.write(address + "\n")
f.close()

#Sum cards in zombie wallets by type
l_zombie_unwrapped = [0]*31
l_zombie_wrappedOfficial = [0]*31
l_zombie_wrappedUnofficial = [0]*31
i = 0
while i <= 30:
    symbol = "CRO" + str(df_cs.iat[i, 0])
    l_zombie_unwrapped[i] = df_all.loc[(df_all['id'].isin(l_id_zombie))
                            & (df_all['symbol'] == symbol), 'unwrapped'].sum()
    l_zombie_wrappedOfficial[i] = df_all.loc[(df_all['id'].isin(l_id_zombie))
                                & (df_all['symbol'] == symbol),
                                'wrappedOfficial'].sum()
    l_zombie_wrappedUnofficial[i] = df_all.loc[(df_all['id'].isin(l_id_zombie))
                                & (df_all['symbol'] == symbol),
                                'wrappedUnofficial'].sum()
    i += 1

#Get timelocked CRO29 cards
#Although it is possible to access these cards, only a fraction of the supply
#    is transferred out yearly by Robek World
l_timelock_unwrapped = [0]*31
l_timelock_unwrapped[29 - 1] = df_all.loc[(df_all['id'] == id_timelock) & 
                            (df_all['symbol'] == "CRO29"), 'unwrapped'].item()

#Calculate total inactive token counts, percent inactive, and total active
l_zombie_supply = [sum(x) for x in zip(l_zombie_unwrapped, 
                l_zombie_wrappedOfficial, l_zombie_wrappedUnofficial,
                l_timelock_unwrapped)]
l_active = [x - y for x, y in zip(l_remain, l_zombie_supply)]

#Add all token count lists to df_cs and df_cs_verb
df_cs_verb = df_cs.copy()
df_cs_verb['Unwrapped Supply'] = l_unwrapped
df_cs_verb['Official Wrapped Supply'] = l_wrappedOfficial
df_cs_verb['Unofficial Wrapped Supply'] = l_wrappedUnofficial
df_cs['Total Supply'] = l_supply
df_cs_verb['Total Supply'] = l_supply
df_cs_verb['Locked/Unwrappable Cards'] = l_lc_burn
df_cs_verb['Burned Cards'] = l_burned
df_cs['Total Burned Cards'] = l_inaccessible
df_cs_verb['Total Burned Cards'] = l_inaccessible
df_cs['Remaining Supply'] = l_remain
df_cs_verb['Remaining Supply'] = l_remain
df_cs_verb['Unwrapped in Inactive Wallets'] = l_zombie_unwrapped
df_cs_verb['wrappedOfficial in Inactive Wallets'] = l_zombie_wrappedOfficial
df_cs_verb['wrappedUnofficial in Inactive Wallets'] = l_zombie_wrappedUnofficial
df_cs_verb['Unwrapped in Timelocked Wallets'] = l_timelock_unwrapped
df_cs['Inactive Wallet Supply'] = l_zombie_supply
df_cs_verb['Inactive Wallet Supply'] = l_zombie_supply
df_cs['Active Supply'] = l_active
df_cs_verb['Active Supply'] = l_active

#Export df_cs and df_cs_verb
f = open("Card_Supply.csv", 'w+')
f.write(df_cs.to_csv(index = False))
f.close
f = open("Card_Supply_Verbose.csv", 'w+')
f.write(df_cs_verb.to_csv(index = False))
f.close

print("Completed successfully!")
