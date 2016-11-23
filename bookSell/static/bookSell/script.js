$(document).ready(function(){
    $(".on_click").click(function(){
        $("#searchBox").css("z-index", "-100");
        $("footer").css("z-index","-100");
        $(".col-md-8").css("z-index","-100");
    });
});

/* Shop By Category */

$(document).ready(function(){
    var obj = {
      ".col-0": [".m-0",".text-0"],
      ".col-1": [".m-1",".text-1"],
      ".col-2": [".m-2",".text-2"],
      ".col-3": [".m-3",".text-3"],
      ".col-4": [".m-4",".text-4"],
      ".col-5": [".m-5",".text-5"],
      ".col-6": [".m-6",".text-6"],
      ".col-7": [".m-7",".text-7"]
    };

    $.each( obj, function( key, value ) {
      $(key).hover(function(){
            $(value[0]).css("opacity", "1");
            $(value[1]).css("visibility", "hidden");
            }, function(){
            $(value[0]).css("opacity", "0.35");
            $(value[1]).css("visibility", "visible");
      });
    });
});

function append_table(){
    //Book Title
    var titles = ["Science <br>Fiction", "Drama", "Action<br> and <br>Adventure", "Romance", "Mystery", "Health",
                  "Children's", "Science", "History", "Biographies"]

    //Image title
    var image_title = ["ScienceFiction", "Drama", "ActionAdventure", "Romance", "Mystery", "Health",
                  "Children", "Science", "History", "Biographies"]

    for(i = 0; i < 8; i++){
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
        link.href = '#';
        media_left.appendChild(link);

        var title = document.createElement('h2');
        title.className = 'text-center text-' + [i];
        title.innerHTML = titles[i];
        col.appendChild(title);

        //Adding images
        var images = document.createElement("img");
        images.src = "static//bookSell/images/books/Biographies.jpg";
        link.appendChild(images);
    }
}

window.onload = function() {
    append_table();
    /*add_book();*/
};

/* Image */


