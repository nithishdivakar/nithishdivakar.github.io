DATE=$(shell date +'%Y-%m-%d')


all: 
	bundle exec jekyll serve


post:
	sh _posts/new_post.template ${DATE} > _posts/${DATE}-new-post.md
    
link:
	sh _links/new_link.template ${DATE} > _links/${DATE}-new-link.md
    
