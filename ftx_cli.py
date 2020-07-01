import traceback
from ftx.client import FtxClient

# In[1]:

'''
Good day, all. My name is Sim (@Simpelalpha) -- usitilizing both hybrid automated/directionary and
automated market making (AMM). This is article, I will walk you through how to build a simpl tool
that has been a great benefit to my trading, a general command line interface that wil allow you
to quickly  navirate and exeute orders on the FTX platform. The script contains for 4 pairs: FTX
client authentication, fetching pertinent data to execute orders, triaging the data, and finally
running the execution script.

Let's get started!

First, we need to instantiate the client under the User class. Here, you input your API
key/secret pair. Here, we are all only instantiating one account, but it's possible to authenticate
multiple accounts, and thus operate the script using multiple accounts.
'''


print('Command Line Interface by Sim (Twitter: @SimpelAlpha)')
print('loading...')

class Cli():
	"""FTX CLI interface class wrapper"""
	def __init__(self, api_key, api_secret):
		print('Authenticating FTX Client...')
		self.client = FtxClient(api_key=api_key, api_secret=api_secret, sub_account_name=None)


	'''
	Following authentication, we create a a few getter methods in order to fetch pertinent data
	required to execute orders. This includes balance, account, and market data. For the sake of
	simplicity, we will be creating a CLI specific to FTX trading pairs priced against USD.

	These getter methods are: get_label_dict, get_balance, get_market, and get_account
	- get_label_dict() allows us to efficiently label and define variables using key:value pairs of
	  dictionaries.
	- get_balance, get_market (data), and get_account methods are specific data that will be useful when building
	  out your own bespoke CLI.
	'''

	@staticmethod
	def get_label_dict(_dict):
		"""Creates global variables we can use later"""
		print(f'Labeling variables in dictionary: {_dict}...')
		for key, value in _dict.items():
			globals()[key] = value

	def get_balance(self):
		"""Fetches our account balance"""
		dict_balance = self.client.get_balances()
		Cli.get_label_dict(dict_balance[1])

	def get_market(self, sym):
		"""Fetches FTX markets"""
		markets = self.client.list_all_markets()
		for markets_ in markets:
			if markets_['name'] == sym:
				Cli.get_label_dict(markets_)

	def get_account(self):
		"""Fetches account information"""
		Cli.get_label_dict(self.client.get_account_info())


	def triage(self, get):
		'''
		Here is the meat of the script. We will be passing a string value ('get') that will contain
		a syntactically correct directive broken up using the split() function.
		'''

		list_get = get.split(' ')
		print(f'Directive list: {list_get}')

		'''
		get balance, account, and market data
		'''

		self.get_balance()
		self.get_account()
		market_ = list_get[0].upper()
		self.get_market(market_)

		'''
		parameters, side & size should be the same regardless of order type
		'''

		side_ = list_get[2]
		total_usdPositionSize = (float(list_get[-1]) * leverage * usdValue)
		amount = total_usdPositionSize/last
		size_ = amount - amount % sizeIncrement

		'''
		order type specific parameters are defined here
		'''
		response = []
		if list_get[1] == 'mark':
			type_ = 'market'
			price_ = None
			print(f'Order Parameters List: { [market_, type_, side_, price_, size_]}')
			response = [market_, type_, side_, price_, size_]
		elif list_get[1] == 'lim':
			type_ = 'limit'
			price_ = float(list_get[3]) - float(list_get[3]) % priceIncrement
			print(f'Order Parameters List: { [market_, type_, side_, price_, size_]}')
			response = [market_, type_, side_, price_, size_]
		elif list_get[1] == 'slim':
			type_ = 'stop_limit'
			price_ = float(list_get[3]) - float(list_get[3]) % priceIncrement
			stop_ = float(list_get[4]) - float(list_get[4]) % priceIncrement
			print(f'Order Parameters List: { [market_, type_, side_, price_, stop_, size_]}')
			response = [market_, type_, side_, price_, stop_, size_]
		elif list_get[1] == 'smark':
			type_ = 'stop_market'
			price_ = None
			stop_ = float(list_get[4]) - float(list_get[4]) % priceIncrement
			print(f'Order Parameters List: { [market_, type_, side_, price_, stop_, size_]}')
			response = [market_, type_, side_, price_, stop_, size_]
		else:
			print('Incorrect Order Type...')

		return response


	def run(self, get=str()):
		"""Parses and executes requested order"""
		order_params = self.triage(get)
		if order_params[1] in ['limit', 'market']:
			try:
				print(f'Creating {order_params[1]} order!...')
				self.client.place_order(
								market=order_params[0],
								side=order_params[2],
								price=order_params[3],
								type=order_params[1],
								size=order_params[4])
			except KeyboardInterrupt:
				pass
			except Exception:
				print(traceback.format_exc())
		elif order_params[1] in ['stop_market', 'stop_limit']:
			try:
				print(f'Creating {order_params[1]} order!...')
				self.client.place_stoploss_order(
								market=order_params[0],
								side=order_params[2],
								triggerPrice=order_params[4],
								orderPrice=order_params[3],
								size=order_params[4])
			except KeyboardInterrupt:
				pass
			except Exception:
				print(traceback.format_exc())


#%%


cli = Cli(api_key="", api_secret="")
while True:
	cli.run(get=input('Get Directive (e.g. "BTC-PERP lim buy 9000 .01"): '))



# %%
