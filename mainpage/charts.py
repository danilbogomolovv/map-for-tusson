import numpy as np
import matplotlib.pyplot as plt

from io import StringIO

def get_terminal_chart(terminals, attr, name, data_type):
	result = {}
	data = {}

	for i in terminals:
		if data_type:
			if getattr(i, attr) not in result.keys():
				result[getattr(i, attr).upper()] = 0
			else:
				result[getattr(i, attr).upper()] = result[getattr(i, attr)] + 1
		else:
			if getattr(i, attr) not in result.keys():
				result[getattr(i, attr)] = 0
			else:
				result[getattr(i, attr)] = result[getattr(i, attr)] + 1

	
	fig = plt.figure(figsize=(12, 7), dpi=80)
	plt.grid(True) 
	plt.bar(result.keys(), result.values())
	plt.title(name)
	imgdata = StringIO()
	fig.savefig(imgdata, format='svg')
	imgdata.seek(0)
	data['img'] = imgdata.getvalue()
	data['result'] = result
	return data

