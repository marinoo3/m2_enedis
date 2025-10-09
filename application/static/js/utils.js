// Download dataURL as file
function downloadDataUrl(dataurl, filename) {
    const link = document.createElement("a");
    link.href = dataurl;
    link.download = filename;
    link.click();
}