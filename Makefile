

build_lang:
	# recompile languages files
	docker-compose run --rm facets-api find i18n -name \*.po -execdir msgfmt knowledge-panel.po -o knowledge-panel.mo \;
