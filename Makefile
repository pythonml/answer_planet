BASEDIR=$(CURDIR)
WEBSITEDIR="/var/www/answer_planet"
rsync_files:
	rsync -avc --delete $(BASEDIR)/ $(WEBSITEDIR)/
