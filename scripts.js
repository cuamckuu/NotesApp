function deleteNote(num) {
    var state = confirm("Are you sure?");
    if (state) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/?action=del&num=" + num, false);
        xhr.send();

        if (xhr.readyState == 4 && xhr.status == 200) {
            //alert("OK state with num: " + num);
            location.reload();
        }
    }
}
