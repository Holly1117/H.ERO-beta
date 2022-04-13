window.onload = function () {
    setYoutube();
    setMenu();
    setCard(null, null, true);
}

function setMenu() {

    $.getJSON("./json/calendar.json", function (dataList) {
        for (var i in dataList) {
            let date_yyyy_mm = dataList[i].date_year + "-" + dataList[i].date_month;
            $("#calendarMenu").prepend("<label class=\"radioLabel\" for=\"menu" + date_yyyy_mm + "\">" + dataList[i].date_year + "年" + dataList[i].date_month + "月" + "</label>");
            $("#calendarMenu").prepend("<input onclick=\"setCardEvent(" + dataList[i].date_year + "," + dataList[i].date_month + ")\" id=\"menu" + date_yyyy_mm + "\" class=\"radioInput filter\" type=\"radio\" name=\"calendarRadio\"/>");
        }
        $("#calendarMenu").prepend("<label class=\"radioLabel\" for=\"menuAll\">ALL</label>");
        $("#calendarMenu").prepend("<input id=\"menuAll\" class=\"radioInput filter\" type=\"radio\" name=\"calendarRadio\"/ checked=\"checked\">");
        $("#menuAll").on("click", () => {
            $("#cardList").children().remove();
            setCard(null, null, true);
        });
    });
}

function setCardEvent(year, month) {
    $("#cardList").children().remove();
    setCard(year, month, false);
}

function setCard(year, month, flag) {
    $.getJSON("./json/hero.json", function (data) {
        for (var i in data) {
            let dateYear = data[i].menu_date_year
            let dateMonth = data[i].menu_date_month
            if (flag || (dateYear == year && dateMonth == month)) {
                console.log("./image/game/" + data[i].game_image);
                $("#cardList").append("<div class=\"cardItem\"><img class=\"cardImage jsModalVideo\" src=\"./image/game/" + data[i].game_image + ".webp\" alt=\"" + data[i].game_name + "\" data-video-id=\"" + data[i].game_youtube + "\"title=\"" + data[i].game_name + "\" onerror=\"this.onerror = null; this.src='https://placehold.jp/300x180.png';\"><p class=\"cardTitle\"><a href=\"" + data[i].game_url + "\" target=\"_blank\" rel=\"noopener noreferrer\" title=\"" + data[i].game_name + "\">" + data[i].game_name + "</a></p><div class=\"cardContentArea\"><div class=\"cardBrand\"><a href=\"" + data[i].brand_url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + data[i].brand_name + "</a></div><div class=\"cardDate\">" + data[i].game_date + "</div></div></div>");
            }
        }
    });
}

function fileCheck(filePath) {
    var filepath = new air.File(filePath);
    return filepath.exists
}

function setYoutube() {
    if ($(".jsModalVideo").length) {
        $(".jsModalVideo").modalVideo({
            channel: "youtube",
            youtube: {
                rel: 0,
                autoplay: 1,
            },
        });
    }
}