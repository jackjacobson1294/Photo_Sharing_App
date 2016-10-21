import os, sys
import hashlib 

seq_num = 0
album_id = 0
for filename in os.listdir('/vagrant/p2/static/images'):
	valid_img_format = filename[-3:]
	if(valid_img_format == 'jpg'):
		temp = filename.split('_', 1)[0]
		if(temp =='sports'):
			album_id = 1
		elif(temp == 'football'):
			album_id = 2
		elif(temp == 'world'):
			album_id = 3
		elif(temp == 'space'):
			album_id = 4;
		m = hashlib.md5(str(album_id) + filename)
		pic_id = m.hexdigest()
		new_name = str(pic_id) + ".jpg"
		print 'INSERT ' + 'INTO ' + 'Photo ' + 'VALUES(' + '\'' +str(pic_id) + '\''  + ', ' + "\'jpg\'" + ', CURRENT_TIMESTAMP());'
		print 'INSERT ' + 'INTO ' + 'Contain ' + 'VALUES(' + str(seq_num) +', ' + str(album_id)+', ' + '\'' +str(pic_id) + '\'' +', \"\"' + ');'
		seq_num = seq_num + 1
		print filename
		os.rename('/vagrant/p2/static/images/' + filename, '/vagrant/p2/static/images/' + new_name)

	

