window.onload = function(){

    setTimeout(function(){

        document.getElementById("splash").style.display = "none";

        document.getElementById("main-content").style.display = "block";

    },3000);

};

function goHome() {
    location.reload();
}

function toggleProfile() {
    document
        .getElementById("profileDropdown")
        .classList.toggle("show");
}

window.onclick = function(event) {

    if (!event.target.matches('.user-btn')) {

        let dropdown =
            document.getElementById("profileDropdown");

        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
};

function playMovie() {
    window.location.href = "/watch/1";
}

function showPlatform(platform){

    document.getElementById("home-content").style.display = "none";

    let cards = document.querySelectorAll(".card");

    cards.forEach(card => {

        card.style.display = "none";

        if(platform === "Netflix" && card.classList.contains("netflix"))
            card.style.display = "block";

        if(platform === "Prime Video" && card.classList.contains("prime"))
            card.style.display = "block";

        if(platform === "Hotstar" && card.classList.contains("hotstar"))
            card.style.display = "block";
    });

    document.getElementById("platform-title").innerHTML =
        platform + " Movies";
}

function showAllMovies(){

    document.getElementById("home-content").style.display = "none";

    document.querySelectorAll(".card").forEach(card => {
        card.style.display = "block";
    });

    document.getElementById("platform-title").innerHTML =
        "All Movies";
}

function showHome(){

    document.getElementById("home-content").style.display = "block";

    document.querySelectorAll(".card").forEach(card => {
        card.style.display = "block";
    });

    document.getElementById("platform-title").innerHTML =
        "Select a Platform";
}

function showTVShows() {

    alert("TV Shows page coming soon!");
}

function showMyList() {

    alert("My List page coming soon!");
}