


function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
}
function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
}



/*------video-section--------*/
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var players = [];

function onYouTubeIframeAPIReady() {
    $('.youtube-video').each(function (i) {
        var frame = $(this);
        var src = frame.attr('src');

        src = UpdateQueryString('enablejsapi', '1', src);
        frame.attr('src', src);
        players.push(new YT.Player($(this).get(0)));
    });
}

function playVideos() {
    for (var i in players) {
        players[i].playVideo();
    }
}

function pauseVideos() {
    for (var i in players) {
        players[i].pauseVideo();
    }
}

function stopVideos() {
    for (var i in players) {
        players[i].stopVideo();
    }
}

// Source: http://stackoverflow.com/a/11654596
// License: https://creativecommons.org/licenses/by-sa/2.0/
// No changes made.
function UpdateQueryString(key, value, url) {
    if (!url) url = window.location.href;
    var re = new RegExp("([?&])" + key + "=.*?(&|#|$)(.*)", "gi"),
        hash;

    if (re.test(url)) {
        if (typeof value !== 'undefined' && value !== null)
            return url.replace(re, '$1' + key + "=" + value + '$2$3');
        else {
            hash = url.split('#');
            url = hash[0].replace(re, '$1$3').replace(/(&|\?)$/, '');
            if (typeof hash[1] !== 'undefined' && hash[1] !== null)
                url += '#' + hash[1];
            return url;
        }
    }
    else {
        if (typeof value !== 'undefined' && value !== null) {
            var separator = url.indexOf('?') !== -1 ? '&' : '?';
            hash = url.split('#');
            url = hash[0] + separator + key + '=' + value;
            if (typeof hash[1] !== 'undefined' && hash[1] !== null)
                url += '#' + hash[1];
            return url;
        }
        else
            return url;
    }
}


/*JS FOR SCROLLING THE ROW OF THUMBNAILS*/ 
$(document).ready(function () {
    $('.vid-item').each(function(index){
      $(this).on('click', function(){
        var current_index = index+1;
        $('.vid-list li').removeClass('active');
        $('.vid-list li:nth-child('+current_index+') .thumb').addClass('active');
      });
    });
    var $list = $('#vid-list li');
    $list.click(function(){
      $list.removeClass('selected');
      $(this).addClass('selected'); 
    });
  });