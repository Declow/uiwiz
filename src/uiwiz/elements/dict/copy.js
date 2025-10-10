document.querySelectorAll(".wiz-copy-content").forEach((el) => {
    el.addEventListener("click", (evt) => {
        var data = evt.currentTarget.getAttribute("data-copy-data");
        navigator.clipboard.writeText(data).then(() => {
            console.log("Text copied to clipboard!");
        }).catch(err => {
            console.error("Failed to copy:", err);
        });
    });
});