from flask import Flask, render_template, request, url_for, send_file
import matplotlib 
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os
from io import BytesIO
import numpy as np
PEOPLE_FOLDER='/home/sundesh/Desktop/flas/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=PEOPLE_FOLDER

@app.route('/')
def input():
	return render_template("form.html")


@app.route("/graph", methods=['GET','POST'])
def showgraph():
	listx=list(map(float,request.form['xaxis'].split(',')))
	listy=list(map(float,request.form['yaxis'].split(',')))
	np_listy=np.array(listy)	
	mean=np.mean(np_listy)
	median=np.median(np_listy)
	x_label=(request.form['x_label'])
	y_label=(str(request.form['y_label']))
	plot_title=('Mean '+str(x_label)+':' +str(mean)+', Median '+str(x_label)+':'+str(median) )
	if (request.form['plot']=='line') :
		j=int(0)
		i=int(0)
		k=int(0)
		for z in range (0, np.size(np_listy)-1):
			for i in range (0,np.size(np_listy)-1):
				if (int(listx[i])>int(listx[i+1])):
					j=listx[i]
					listx[i]=listx[i+1]
					listx[i+1]=j
					k=listy[i]
					listy[i]=listy[i+1]
					listy[i+1]=k
		
		plt.figure()
		plt.plot(listx,listy)
	elif (request.form['plot']=='scatter') :
		plt.figure()
		plt.scatter(listx,listy)
	elif (request.form['plot']=='bar') :	
		plt.figure()
		plt.bar(listx,listy)
	else:
	    plt.figure()
	    plt.bar(listx,listy)
	plt.ylabel(x_label)
	plt.xlabel(y_label)
	plt.title(plot_title)
	img = BytesIO()
	plt.savefig(img, format='png')
	img.seek(0)
	return send_file(img, mimetype='image/png')

app.run(debug=True)
