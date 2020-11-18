
_GIF87a = bytes.fromhex("474946383761")
_GIF89a = bytes.fromhex("474946383961")

_TIFFle = bytes.fromhex("49492A00")
_TIFFbe = bytes.fromhex("4D4D002A")

_JPGa = bytes.fromhex("FFD8FFDB")
_JPG_JFIF = bytes.fromhex("FFD8FFE000104A4649460001")
_JPGb = bytes.fromhex("FFD8FFEE")
_JPG_EXIF = bytes.fromhex("FFD8FFE1")

_PDF = bytes.fromhex("255044462D")
_PNG = bytes.fromhex("89504E470D0A1A0A")

mtypes = {
	_GIF87a: 'gif',
	_GIF89a: 'gif',
	_TIFFle: 'tif',
	_TIFFbe: 'tif',
	_PDF: 'pdf',
	_PNG: 'png',
	_JPGa: 'jpg',
	_JPG_JFIF: 'jpg',
	_JPG_EXIF: 'jpg',
	_JPGb: 'jpg'
}


def starts_with(data, prefix):
	if len(data) < len(prefix):
		return False

	i = 0
	for (d,p) in zip(data, prefix):
#		dt = type(d)
#		pt = type(p)
#		print( f"d: {d} ({dt}), p: {p} ({pt})")
		if d != p:
			return False
		i = i + 1
	return True

def is_gif(data):
	return starts_with(data, _GIF89a) or starts_with(data, _GIF87a)

def is_tif(data):
	return starts_with(data, _TIFFle) or starts_with(data, _TIFFbe)

def is_png(data):
	return starts_with(data, _PNG)

def is_pdf(data):
	return starts_with(data, _PDF)

def get_mtype(data):

	for prefix,mtype in mtypes.items():
		if starts_with(data, prefix):
#			print(f"Found mtype prefix for {mtype}")
			return mtype

	return None

if __name__ == "__main__":

	files = [ "scan.png", "scan.pdf"]

	for f in files:
		fin = open(f, "rb")
		header = fin.read(16)
		n_bytes = len(header)
#		print(f"{n_bytes} read from file {f}")
		fin.close()
		mtype = get_mtype(header)
		print(f"mtype of file {f} is: {mtype}")

#	data = bytes.fromhex("00000102040402030230404044")
#	mtype = get_mtype(data)
#	print(f"Data has mtype: {mtype}")
