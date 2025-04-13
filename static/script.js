function getResponse() {
    let userText= $("#textInput").val();
    if (userText != "") {
        let userHtml= '<p class="userText"><span>' + userText + '</span></p>';
        $("#textInput").val(""); //clear input
        $("#chatbox").append(userHtml);
        document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});

        let loadingBubble = '<p class="botText loadingBubble"><span>...</span></p>';
        $("#chatbox").append(loadingBubble);
        document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
    }
    let user = $("#loggedUserinp").val();
    $.get("/get", { msg: userText, user:user }).done(function(data) {
        $(".loadingBubble").remove();
        if (data !== "") {
            let formattedText = marked.parse(data);
            var botHtml = '<div class="botText"><span>' + formattedText + '</span></div>';
            $("#chatbox").append(botHtml);
            document.getElementById('userInput').scrollIntoView({ block: 'start', behavior: 'smooth' });
        }
    });
}

function getInitialGreeting() {
    $.get("/greet").done(function(data) {
        var botHtml = '<p class="botText"><span>' + data + '</span></p>';
        $("#chatbox").append(botHtml);
        document.getElementById('#userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
        }
    );
}

$("#textInput").keypress(function(e) {
    if (e.which == 13) {
        getResponse();
    }
});
$("#buttonInput").click(function() {
    getResponse();
});