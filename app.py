# app.py
from flask import Flask, render_template, send_from_directory, redirect, url_for           # import flask
from flask import request
from werkzeug.utils import secure_filename
from os import listdir, makedirs
from os.path import isfile, join
import os.path, time
import subprocess
import os
import datetime
import hashlib
import docweb
import uuid
import sys
import re
from docweb.ocr import ocr_from_image_file, ocr_from_pdf_file
from flask_dropzone import Dropzone

STOPWORDS = "ab, aber, abgesehen, alle, allein, aller, alles, als, am, an, andere, anderen, anderenfalls, anderer, anderes, anstatt, auch, auf, aus, aussen, außen, ausser, außer, ausserdem, außerdem, außerhalb, ausserhalb, behalten, bei, beide, beiden, beider, beides, beinahe, bevor, bin, bis, bist, bitte, da, daher, danach, dann, darueber, darüber, darueberhinaus, darüberhinaus, darum, das, dass, daß, dem, den, der, des, deshalb, die, diese, diesem, diesen, dieser, dieses, dort, duerfte, duerften, duerftest, duerftet, dürfte, dürften, dürftest, dürftet, durch, durfte, durften, durftest, durftet, ein, eine, einem, einen, einer, eines, einige, einiger, einiges, entgegen, entweder, erscheinen, es, etwas, fast, fertig, fort, fuer, für, gegen, gegenueber, gegenüber, gehalten, geht, gemacht, gemaess, gemäß, genug, getan, getrennt, gewesen, gruendlich, gründlich, habe, haben, habt, haeufig, häufig, hast, hat, hatte, hatten, hattest, hattet, hier, hindurch, hintendran, hinter, hinunter, ich, ihm, ihnen, ihr, ihre, ihrem, ihren, ihrer, ihres, ihrige, ihrigen, ihriges, immer, in, indem, innerhalb, innerlich, irgendetwas, irgendwelche, irgendwenn, irgendwo, irgendwohin, ist, jede, jedem, jeden, jeder, jedes, jedoch, jemals, jemand, jemandem, jemanden, jemandes, jene, jung, junge, jungem, jungen, junger, junges, kann, kannst, kaum, koennen, koennt, koennte, koennten, koenntest, koenntet, können, könnt, könnte, könnten, könntest, könntet, konnte, konnten, konntest, konntet, machen, macht, machte, mehr, mehrere, mein, meine, meinem, meinen, meiner, meines, meistens, mich, mir, mit, muessen, müssen, muesst, müßt, muß, muss, musst, mußt, nach, nachdem, naechste, nächste, nebenan, nein, nichts, niemand, niemandem, niemanden, niemandes, nirgendwo, nur, oben, obwohl, oder, oft, ohne, pro, sagte, sagten, sagtest, sagtet, scheinen, sehr, sei, seid, seien, seiest, seiet, sein, seine, seinem, seinen, seiner, seines, seit, selbst, sich, sie, sind, so, sogar, solche, solchem, solchen, solcher, solches, sollte, sollten, solltest, solltet, sondern, statt, stets, tatsächlich, tatsaechlich, tief, tun, tut, ueber, über, ueberall, überll, um, und, uns, unser, unsere, unserem, unseren, unserer, unseres, unten, unter, unterhalb, usw, viel, viele, vielleicht, von, vor, vorbei, vorher, vorueber, vorüber, waehrend, während, wann, war, waren, warst, wart, was, weder, wegen, weil, weit, weiter, weitere, weiterem, weiteren, weiterer, weiteres, welche, welchem, welchen, welcher, welches, wem, wen, wenige, wenn, wer, werde, werden, werdet, wessen, wie, wieder, wir, wird, wirklich, wirst, wo, wohin, wuerde, wuerden, wuerdest, wuerdet, würde, würden, würdest, würdet, wurde, wurden, wurdest, wurdet, ziemlich, zu, zum, zur, zusammen, zwischen".split(", ")

ALLOWED_EXTENSIONS = [ "pdf", "png", "jpg" ]
text_data = ""
saved_file = None
all_words = set()
words = []
word_vector = None
doc_freq = {}
word_pattern = re.compile("[a-zA-Z0-9_\\-]*")

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d")

def modification_time(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S")

def md5(xs):
	return (hashlib.md5(str(xs).encode('utf-8')).hexdigest())

app = Flask("DocWeb", static_folder='static')             # create an app instance
app.config['UPLOAD_FOLDER'] = "incoming"
app.config['DROPZONE_REDIRECT_VIEW'] = "index"
app.config['DROPZONE_DEFAULT_MESSAGE'] = "PDF Dateien/Scans auf diese Fläche ziehen oder klicken."
dropzone = Dropzone(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_word(s):
	return word_pattern.match(s)

@app.route('/ocr', methods=['POST'])
def ocr_post():
	if request.method == 'POST':
		print(f"uploaded files: {request.files}")

		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			objType = type(file)
			print(f"type of file object is: {objType}")
			fileId = str(uuid.uuid4())

			output = os.path.join(app.config['UPLOAD_FOLDER'], fileId + ".pdf")
			file.save(output)
			print(f"Writing uploaded file to {output}")

			try:
				txt = ocr_from_pdf_file(output)
				print( f"extracted text: {txt}")

				txt_file = os.path.join("incoming", fileId + ".txt")
				tf = open(txt_file, "w")
				tf.write(txt)
				tf.close()
				print(f"Wrote OCR data to {txt_file}")
				print("Returning render_template...")
				global text_data
				text_data = txt
				global saved_file
				saved_file = fileId + ".pdf"

				global words
				global word_vector
				global all_words
				ws = txt.lower().split()
				words = [w for w in ws if is_word(w)]

				def count_word(w, ws):
					cnt = 0
					for x in ws:
						if w == x:
							cnt = cnt + 1
					return cnt

				word_list = set(words)
				for w in word_list:
					all_words.add(w)
					if w not in doc_freq:
						doc_freq[w] = 1
					else:
						df = doc_freq[w] 
						doc_freq[w] = df + 1

				word_vector = [ count_word(w, words) for w in all_words ]

#				session['saved_file'] = saved_file
#				return render_template("index.html", text=txt)

			except Exception as e:
				print("Error while extracting OCR data...")
				print("Error: {}".format(sys.exc_info()))
				pass

			return redirect(url_for('index'))

	print("global redirect to {}".format("index"))
	return redirect(url_for('index'))

@app.route("/api/ocr",methods=["PUT"])
def ocr():
#	print("reading OCR data from {}".format(request.uri))
	data = request.data
	n_bytes = len(data)
	print(f"Request contains {n_bytes} of data")
	tmpId = str(uuid.uuid4())
	tmpFile = f"/tmp/ocr-input-{tmpId}"
	file = open(tmpFile, "wb")
	file.write(data)
	file.close()
#	print(f"Wrote {n_bytes} bytes to {tmpFile}")
	txt = ocr_from_image_file(tmpFile)
#	print(f"Text is: {txt}")
	os.remove(tmpFile)
	return txt

def setup():
    makedirs("data/.thumbs", exist_ok=True)
    makedirs("incoming/.thumbs", exist_ok=True)

@app.route("/")
def index():
	print("Handling / request...")
	return render_template("index.html", text=text_data, saved_file=saved_file, words=all_words, word_vector=word_vector)

if __name__ == "__main__":        # on running python app.py
    setup()
    app.run(host="0.0.0.0")                     # run the flask app
