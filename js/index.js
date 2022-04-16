window.onload = function () {
    //setYoutube();
    setMenu();
    setCard(null, null, true);
}

function setMenu() {

    $.getJSON("./json/calendar.json", function (dataList) {
        var $calendar = $("#calendarMenu");
        var calendarMenuTag = [];
        calendarMenuTag.push("<input id=\"menuAll\" class=\"radioInput filter\" type=\"radio\" name=\"calendarRadio\"/ checked=\"checked\">");
        calendarMenuTag.push("<label class=\"radioLabel\" for=\"menuAll\">ALL</label>");
        dataListLength = dataList.length;
        for (let i = dataListLength - 1; i >= 0; i--) {
            let date_yyyy_mm = dataList[i].date_year + "-" + dataList[i].date_month;
            let setCardEventMethod = "setCardEvent(" + dataList[i].date_year + "," + dataList[i].date_month + ")";
            let inputId = "menu" + date_yyyy_mm;
            let menuName = dataList[i].date_year + "年" + dataList[i].date_month + "月";
            calendarMenuTag.push("<input onclick=\"" + setCardEventMethod + "\" id=\"" + inputId + "\" class=\"radioInput filter\" type=\"radio\" name=\"calendarRadio\"/>");
            calendarMenuTag.push("<label class=\"radioLabel\" for=\"" + inputId + "\">" + menuName + "</label>");
        }
        $calendar[0].innerHTML = calendarMenuTag.join("");
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
        var $carList = $("#cardList");
        var cardListTag = [];

        for (var i in data) {
            var dateYear = data[i].menu_date_year;
            var dateMonth = data[i].menu_date_month;
            if (flag || (dateYear == year && dateMonth == month)) {
                var kindsLogo = "";
                if (data[i].game_kinds == "(NS)") {
                    kindsLogo = "<img class=\"hardLogo\" src=\"./image/logo/ns-logo.png\">";
                } else if (data[i].game_kinds == "(PS4)") {
                    kindsLogo = "<img class=\"hardLogo\" src=\"./image/logo/ps-logo.png\">";
                } else if (data[i].game_kinds == "(XBO)") {
                    kindsLogo = "<img class=\"hardLogo\" src=\"./image/logo/xbox-logo.svg\">";
                }
                let youtubeTag = "data-video-id=\"" + data[i].game_youtube + "\"";
                let imageSrc = "./image/game/" + data[i].game_image + ".png";
                let imageTag = "<img class=\"cardImage jsModalVideo\" src=\"" + imageSrc + "\" title=\"" + data[i].game_name + "\" onerror=\"this.onerror = null; this.src='https://placehold.jp/300x180.png';\" loading=\"lazy\">" + kindsLogo;
                let ImageLinkTag = "<a href=\"" + data[i].game_url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + imageTag + "</a>";
                let aTag = "<a href=\"" + data[i].game_url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + data[i].game_name + "</a>";
                let titleLinkTag = "<p class=\"cardTitle\">" + aTag + "</p>";
                let brandTag = "<div class=\"cardBrand\"><a href=\"" + data[i].brand_url + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + data[i].brand_name + "</a></div>";
                let dateTag = "<div class=\"cardDate\">" + data[i].game_date + "</div>";
                let contentAreaTag = "<div class=\"cardContentArea\">" + brandTag + dateTag + "</div>";
                cardListTag.push("<div class=\"cardItem\">" + ImageLinkTag + titleLinkTag + contentAreaTag + "</div>");
            }
        }

        $carList[0].innerHTML = cardListTag.join("");
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