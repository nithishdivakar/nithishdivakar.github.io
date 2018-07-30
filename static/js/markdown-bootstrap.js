$("article.post-content p").each(function(index){
	$(this).addClass("text-justify")
});

$("article.post-content img").each(function(index){
	$(this).addClass("img-fluid")
});



$("article.post-content h2").each(function(index){
  $(this).replaceWith(function() {
    return $("<h4>", {
      "class": this.className + " mt-2",
      html: $(this).html()
    });
  });
});


$("article.post-content h1").each(function(index){
  $(this).replaceWith(function() {
    return $("<h3>", {
      "class": this.className + " mt-5 font-weight-bold",
      html: $(this).html()
    });
  });
});



$("article.post-content pre.highlight>code").each(function(index,block){
  hljs.highlightBlock(block);
});


