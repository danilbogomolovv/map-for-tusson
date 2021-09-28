import numpy as np
import matplotlib.pyplot as plt

from io import StringIO

def get_terminal_chart(terminals, attr, name, pie_or_bar):
	result = {}
	data = {}
	bars = []
	for i in terminals:
		if attr != 'cstatus':
			if str(getattr(i, attr)) not in result.keys():
				result[str(getattr(i, attr)).upper()] = 1

			else:
				result[str(getattr(i, attr)).upper()] = result[getattr(i, attr)] + 1
				
		else:
			if getattr(i, attr) not in result.keys():
				result[getattr(i, attr)] = 1
			else:
				result[getattr(i, attr)] = result[getattr(i, attr)] + 1

	
	fig = plt.figure(figsize=(12, 7), dpi=80)
	plt.grid(True) 
	
	plt.title(name)
	if pie_or_bar == 'pie':
		plt.pie(result.values(), labels = result.keys(), startangle = 90)
	elif pie_or_bar == 'bar':
		plt.bar(result.keys(), result.values(), width = 0.5)

	imgdata = StringIO()
	fig.savefig(imgdata, format='svg')
	imgdata.seek(0)
	data['img'] = imgdata.getvalue()
	data['result'] = result
	return data

