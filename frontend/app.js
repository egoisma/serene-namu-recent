$(document).ready(function() {
    paperWidth = 800;
    paperHeight = 400;
    paper = Raphael(document.getElementById('svg'), paperWidth, paperHeight);
    paper.rect(0, 0, paperWidth, paperHeight);

    //var audio = new Audio("./sound/waterdrop.mp3");
    //audio.volume=1;

    timer_getData = setInterval(getData, 1000);
});

function sleep(ms) { // 다른 곳에서 가져온 코드
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getData() {
    $.ajax({
        type : 'GET',
        url : 'http://localhost:5000/data',
        data : {},
        success : function(data) {
            
            var wiki = data["wiki"];
            for(var i=0; i<wiki.length; i++) {
                var fontSize = (Math.abs(wiki[i]["size"])>50 ? 50 : Math.abs(wiki[i]["size"]/4.0)+18.0);

                var x = Math.random()*(paperWidth-fontSize*(wiki[i]["name"].length+1))+fontSize*(wiki[i]["name"].length+1)/2;
                var y = Math.random()*(paperHeight-(fontSize+2))+(fontSize+2)/2;
                var color = wiki[i]["size"]>=0 ? 'green' : 'red';

                var text = paper.text(x, y, wiki[i]["name"]); // var 사용하면 변수의 scope가 function 최상단이 된다는데..
                console.log("new wiki: " + wiki[i]["name"]);
                //audio.play(); // not working

                text.attr({
                    'fill' : color,
                    'font-size' : fontSize,
                    'font-family' : '돋움',
                    'fill-opacity' : 0.05
                });

                var incOpacity = function() {
                    text.attr({
                    'fill-opacity' : text.attr('fill-opacity')+0.05
                    });
                };
                
                var decOpacity = function() {
                    text.attr({
                    'fill-opacity' : text.attr('fill-opacity')-0.05
                    });
                };

                var timer_incOpacity = setInterval(function() {
                    if(text.attr('fill-opacity')<1) incOpacity();
                    else clearInterval(timer_incOpacity);
                }, 50);

                setTimeout(function() {
                    var timer_decOpacity = setInterval(function() {
                        if(text.attr('fill-opacity')>0) decOpacity();
                        else {
                            clearInterval(timer_decOpacity);
                            text.remove();
                        }
                    }, 50);
                }, 7000);

                sleep(300);
            }
        },
        error : function() {
            alert("Get Failed");
            clearInterval(timer_getData);
        }
    })
}
function start() {
    clearInterval(timer_getData);
    timer_getData = setInterval(getData, 1000);
    document.getElementById("state_getdata").innerHTML = "On";
}
function stop() {
    clearInterval(timer_getData);
    document.getElementById("state_getdata").innerHTML = "Off";
}