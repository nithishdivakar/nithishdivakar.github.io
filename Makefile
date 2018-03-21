serve:
	bundle exec jekyll serve --drafts

build:
	bundle exec jekyll build

post:
	@echo 'new post      : bundle exec jekyll post "My New Post"'
	@echo 'New draft     : bundle exec jekyll draft "My new draft"'
	@echo 'Publish draft : bundle exec jekyll publish _drafts/my-new-draft.md'
	@echo 'or            : bundle exec jekyll publish _drafts/my-new-draft.md --date 2014-01-24'
