// var $ = require("./jquery-1.10.1.js");
window.onload=function () {
    autoheight();
    function autoheight(){
        //获取浏览器窗口高度
        var winHeight=0;
        if (window.innerHeight)
            winHeight = window.innerHeight;
        else if ((document.body) && (document.body.clientHeight))
            winHeight = document.body.clientHeight;
        //通过深入Document内部对body进行检测，获取浏览器窗口高度
        if (document.documentElement && document.documentElement.clientHeight)
            winHeight = document.documentElement.clientHeight;

        document.getElementsByClassName("team")[0].style.height= winHeight*0.8+"px";
        document.getElementsByClassName("result")[0].style.height= winHeight*0.2+"px";
        document.getElementsByClassName("result")[0].style.top= winHeight*0.8+"px";
    }
    window.onresize=autoheight;

    var teamChild=document.getElementsByClassName("team")[0].children;
    for(var i=2;i<32;i++){
        if(i<10){
            teamChild[i].style.top='7%';
            teamChild[i].style.left=4+12*(i-2)+"%";
        }else if(i>=10 && i<17){
            teamChild[i].style.top='28.5%';
            teamChild[i].style.left=4+12*(i-10)+"%";
        }else if(i>=17 && i<25){
            teamChild[i].style.top='57%';
            teamChild[i].style.left=4+12*(i-17)+"%";
        }else{
            teamChild[i].style.top='78.5%';
            teamChild[i].style.left=4+12*(i-25)+"%";
        }
    }

    var num=0;
    var winTeamName = null;
    var loseTeamName = null;
    var teamOneImg=document.getElementsByClassName("team_one_img")[0];
    var teamTwoImg=document.getElementsByClassName("team_two_img")[0];
    var open=document.getElementsByClassName("result")[0];
    for(var j = 32;j < 62;j++){
        teamChild[j].index=j;
        teamChild[j].onclick=function () {
            open.style.display="block";
            if(num===0){
                winTeamName = this.id;
                var str = winTeamName.split("_")
                var str_new = str.join(" ");
                winTeamName = str_new;
                teamOneImg.src='./images/'+(this.index-31)+'.png';
                console.log(teamOneImg);
                num++;
            }else if(num===1){
                loseTeamName = this.id;
                var str = loseTeamName.split("_")
                var str_new = str.join(" ");
                loseTeamName = str_new;
                teamTwoImg.src='./images/'+(this.index-31)+'.png';
                console.log(teamTwoImg);
                num++;
            }
        }
    }
    var emptyButton=document.getElementsByClassName("empty")[0];
    var determineButton=document.getElementsByClassName("determine")[0];
    emptyButton.onclick=function () {
        teamOneImg.src='';
        teamTwoImg.src='';
        num=0;
    }
    $(".determine").click(function () {
        var sInfo = {
            winTeam:winTeamName,
            loseTeam:loseTeamName
        };
        $.ajax({
            url:"/user/prediction",
            type:"post",
            dataType:"json",
            data: sInfo,
            async:false,
            success: function (msg) {
                console.log(msg);
                var win = msg[0].WIN;
                var lose = msg[0].LOSE;
                alert(win+"获胜的概率为"+((msg[0].Probability)*100).toFixed(2) + "%");
            }
        })
    });
};