function getResponse() {
    let userText= $("#textInput").val();
    if (userText != "") {
    let userHtml= '<p class="userText"><span>' + userText + '</span></p>';
<<<<<<< HEAD
    $("#textInput").val(""); 
    $("#chatbox").append(userHtml);
    document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
=======
        $("#textInput").val(""); //clear input
        $("#chatbox").append(userHtml);
        document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    }
>>>>>>> a7e5dfcb94db56cea39f264cff8ab588967a5f38
    $.get("/get", { msg: userText }).done(function(data) {
        if (data != "") {
            var botHtml = '<p class="botText"><span>' + data + '</span></p>';
            $("#chatbox").append(botHtml);
            document.getElementById('#userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
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
