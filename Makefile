BASEDIR=$(CURDIR)
WEBSITEDIR="/var/www/answer_planet"
rsync_files:
	rsync -avc --exclude '.git' --exclude 'tests' --delete $(BASEDIR)/ $(WEBSITEDIR)/
