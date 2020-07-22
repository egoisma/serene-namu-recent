let start, stop;

(() => {
    'use strict';
    
    const PAPER_WIDTH = 800;
    const PAPER_HEIGHT = 400;
    const OPAC_TRANS_SPEED = 0.05;

    let timer_getData;
    let paper;

    $(document).ready(() => {
        paper = Raphael(document.getElementById('svg'), PAPER_WIDTH, PAPER_HEIGHT);
        paper.rect(0, 0, PAPER_WIDTH, PAPER_HEIGHT);

        //var audio = new Audio("./sound/waterdrop.mp3");
        //audio.volume=1;

        timer_getData = setInterval(getData, 1000);
    });

    function sleep(ms) { // 다른 곳에서 가져온 코드
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function getData() {
        fetch('http://localhost:5000/data')
            .then((res) => {
                res.json().then((json) => {
                    const wiki = json["wiki"];

                    for(let i=0; i<wiki.length; i++) {
                        let fontSize = (Math.abs(wiki[i]["size"])>50 ? 50 : Math.abs(wiki[i]["size"]/4.0)+18.0);

                        let x = Math.random()*(PAPER_WIDTH-fontSize*(wiki[i]["name"].length+1))+fontSize*(wiki[i]["name"].length+1)/2;
                        let y = Math.random()*(PAPER_HEIGHT-(fontSize+2))+(fontSize+2)/2;
                        let color = wiki[i]["size"]>=0 ? 'green' : 'red';

                        let text = paper.text(x, y, wiki[i]["name"]);

                        console.log("new wiki: " + wiki[i]["name"]);
                        //audio.play(); // not working

                        text.attr({
                            'fill' : color,
                            'font-size' : fontSize,
                            'font-family' : '돋움',
                            'fill-opacity' : 0.05
                        });

                        let incOpacity = () => {
                            text.attr({
                            'fill-opacity' : text.attr('fill-opacity') + OPAC_TRANS_SPEED
                            });
                        };
                        
                        let decOpacity = () => {
                            text.attr({
                            'fill-opacity' : text.attr('fill-opacity') - OPAC_TRANS_SPEED
                            });
                        };

                        let timer_incOpacity = setInterval(() => {
                            if(text.attr('fill-opacity')<1) incOpacity();
                            else clearInterval(timer_incOpacity);
                        }, 50);

                        setTimeout(() => {
                            let timer_decOpacity = setInterval(() => {
                                if(text.attr('fill-opacity')>0) decOpacity();
                                else {
                                    clearInterval(timer_decOpacity);
                                    text.remove();
                                }
                            }, 50);
                        }, 7000);

                        sleep(300);
                    }
                })
            })
            .catch((err) => {
                alert("Get Failed");
                clearInterval(timer_getData);
            });
    }

    start = () => {
        clearInterval(timer_getData);
        timer_getData = setInterval(getData, 1000);
        document.getElementById("state_getdata").innerHTML = "On";
    }

    stop = () => {
        clearInterval(timer_getData);
        document.getElementById("state_getdata").innerHTML = "Off";
    }
})();
