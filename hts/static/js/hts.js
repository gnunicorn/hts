setTimeout(function() {
    var timer = null;
    var cur_val = null;
    function search() {
        var value = $("#search-input").val();
        cur_val = value;
        fetch("/search/?query=" + value)
        .then(resp => resp.text())
        .then(body => {
            if (cur_val !== value) {
                // have been updated, ignore
                return
            }

            $("#search-spinner").hide();

            var results = $("#search-results");
            console.log(body);
            results.html(body);
            results.show();
        });
    }
    
    // delayed
    $("#search-input").keyup(function() {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
        $("#search-spinner").show();
        $("#search-results").hide();

        timer = setTimeout(search, 300);
    });
    $("#search-spinner").hide();
    $("#search-results").hide();
}, 200)