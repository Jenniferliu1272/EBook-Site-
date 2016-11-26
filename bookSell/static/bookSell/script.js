$(document).ready(function(){
    $(".on_click").click(function(){
        $("#searchBox").css("z-index", "-100");
        $("footer").css("z-index","-100");
        $(".col-md-8").css("z-index","-100");
        $("button").css("z-index", "-100");
    });
});

/* Shop By Category */

function UrlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}

function append_table(){
    //Book Title
    var titles = ["Science<br>fiction", "Drama", "Action and<br>Adventure", "Romance", "Mystery", "Health",
                  "Children's", "Science", "History", "Biographies"]

    //Image title
    var image_title = ["ScienceFiction", "Drama", "ActionAdventure", "Romance", "Mystery", "Health",
                  "Children", "Science", "History", "Biographies"]

    for(i = 0; i < titles.length; i++){
        var col = document.getElementsByClassName("col-" + i)[0];

        //Append Media
        var media = document.createElement('div');
        media.className = 'media m-' + [i];
        col.appendChild(media);

        //Append  Media Left
        var getMedia = document.getElementsByClassName("media")[i];
        var media_left = document.createElement('div');
        media_left.className = 'media-left media-middle';

        getMedia.appendChild(media_left);

        //Append links
        var link = document.createElement('a');
        var reset = titles[i].replace(/<br>/, "%20");
        if( i == 2 ){
            link.href = 'genre/' + "Action%20and%20Adventure";
        }
        else{
            link.href = 'genre/' + reset + '/';
        }
        media_left.appendChild(link);

        var title = document.createElement('h5');
        title.className = 'text-' + [i];
        title.innerHTML = titles[i];
        col.appendChild(title);

        //Adding images
        var images = document.createElement("img");
        if( UrlExists('static/bookSell/images/books/' + image_title[i] + ".jpg" ) == false ){
           images.src = "static/bookSell/images/books/default.png"
        }
        else{
           images.src = "static/bookSell/images/books/" + image_title[i] + ".jpg";
        }
        link.appendChild(images);
    }
}

/* Swipe function, maybe I will implement
 * If I have time */
function swipe_left(){

    var start;
    var end;
    for(var i=0; i < 10; i++){
        //First element I see that is not hidden
        if( $(".book-" + i).css('visibility') === 'visible' ){
            start = i;
            break;
        }
    }
    end = start + 5;
    $(".book-" + end).css('visibility', 'hidden');
    start -= 1;
    $(".book-" + start).css('visibility', 'visible');
}

window.onload = function() {
    append_table();
};

/* Image */


