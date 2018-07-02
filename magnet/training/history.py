class History(dict):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.buffer = {}

	def find(self, key):
		return {k: self[k] for k in self.keys() if key in k}

	def append(self, key, value, validation=False, buffer=False):
		if validation: key = 'val_' + key

		if not buffer:
			try: self[key].append(value)
			except KeyError: self[key] = [value]
			return

		try:
			self.buffer[key].append(value)
			if self.buffer_size > 0 and len(self.buffer[key]) > self.buffer_size:
				self.buffer[key].pop(0)

		except KeyError: self.buffer[key] = [value]

	def show(self, key=None, log=False, x_key=None, xlabel=None):
		from matplotlib import pyplot as plt
		if key is None:
			for k in self.keys(): self.show(k, log)
			return

		y = self[key]
		if len(y) == 0: return
		if len(y) == 1:
			print(key, '=', y)
			return

		if x_key is None: x = list(range(len(y)))
		elif isinstance(x_key, (tuple, list)): x = x_key
		else: x = self[x_key]

		plt.plot(x, y, label='training')
		try:
			y_val = self['val_' + key]
			if len(y_val) == len(y):
				plt.plot(x, y_val, label='validation')
				plt.legend()
		except KeyError: pass

		if log: plt.yscale('log')

		plt.ylabel(key.title())
		if isinstance(xlabel, str):
			plt.xlabel(xlabel)
			plt.title(f'{key.title()} vs {xlabel.title()}')
		elif isinstance(x_key, str):
			plt.xlabel(x_key)
			plt.title(f'{key.title()} vs {x_key.title()}')
		else: plt.title(key.title())
		plt.show()

	def flush(self, key=None):
		if key is None:
			for k in self.buffer.keys(): self.flush(k)
			return

		value = self.buffer[key]
		if len(value) == 0: return

		value = sum(value) / len(value) # Mean

		try: self[key].append(value)
		except KeyError: self[key] = [value]
		finally:
			if self.buffer_size < 0: self.buffer[key] = []