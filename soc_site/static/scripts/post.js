/*
$( document ).ready(function() {
    //console.log($('.roman'))
})

//console.log($('.post_content'))

$('body').on('DOMSubtreeModified', '.post_content', function(){
    //console.log($(".post_content img"))
    //console.log($(".post_content img").parent().find('figure'))
    if($(".post_content p > img").length > 0 ){

        console.log($(".post_content p > img").length)
        $(".post_content p > img").wrapAll("<div></div>")
        return
        console.log($(".post_content p > img").length)

    }
})
*/
