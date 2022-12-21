let currentVideo = {};
let url = "";
function spinner(v) {
    if (v) {
        $("#loading").css("opacity", "1").css("display", "block");

    } else {
        $("#loading").css("opacity", "0").css("display", "none");
    }
}

function vInfo(v) {
    if (v) {
        $("#video-info").css("opacity", "1").css("display", "flex");
    } else {
        $("#video-info").css("opacity", "0").css("display", "none");
    }
}

function downloadSrc(resolution) {
    let format = currentVideo.format;
    spinner(true);
    vInfo(false);
    fetch("/download?url=" + url + "&format=" + resolution)
        .then(resp => resp.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            // the filename you want
            if (resolution === "audio") {
                a.download = currentVideo.title + ".mp3";
            } else {
                a.download = currentVideo.title + ".mp4";
            }
            spinner(false);
            vInfo(true);
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(() => alert('Download failed.'));
}

function lookup() {
    vInfo(false);
    spinner(false);
    // get #searchbar value
    let search = $("#searchbar").val();
    if (search.length > 0) {
        // check if search is a valid URL
        if (search.includes("youtube.com/watch?v=") || search.includes("youtu.be/")) {
            url = search;
            spinner(true);
            // send url
            $.get("/info?url=" + search, function (data) {
                spinner(false);
                vInfo(true);
                currentVideo = data;
                $(".video-title").html(data.title);
                $(".video-length").html(data.length);
                $(".card-img-top").attr("src", data.thumbnail);
                let formats = data.format;
                $("#drop").html("");
                for (let i = 0; i < formats.length; i++) {
                    let format = formats[i];
                    $("#drop").append(`<a class="dropdown-item" href="#" onclick="downloadSrc('${format.resolution}');">${format.resolution} - ${format.format}</a>`);
                }
            });
        }
    }
}