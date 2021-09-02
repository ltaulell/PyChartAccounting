/**
 * @author Damien LE BORGNE
 */


 function loadGroups(name){
    console.log("fromsetup.js");
    $.getJSON('/output/'+name, function(data, status, xhr){

        if(data["groupes"].length > 1){
            var options = '<option value="Tout" selected>Tout</option>';
        }else{
            var select = "selected";
            var options = '<option value="Tout">Tout</option>';
        }
        
        for (var i = 0; i < data["groupes"].length; i++ ) {
            options += '<option value="' + data["groupes"][i]+ '" '+select+'>' + data["groupes"][i] + '</option>';
            select = "";
        }
        // console.log(data["groupes"]);
        $("#groups").html(options);  
    });
}

function read_cookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function set_cookie(name, value) {
    document.cookie = name + '=' + value + '; Path=/;';
}

function delete_cookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function formsetup(data) {

    delete_cookie("annee");
    delete_cookie("debut");
    delete_cookie("fin");
    delete_cookie("queue");
    delete_cookie("cluster");
    delete_cookie("groupe");
    delete_cookie("users");

    if (data.hasOwnProperty('Année')) {
        set_cookie("annee", data["Année"]);
    }

    if (data.hasOwnProperty('Debut')) {
        set_cookie("debut", data["Debut"]);
        set_cookie("fin", data["Fin"]);
    }

    if (data.hasOwnProperty('queue')) {
        set_cookie("queue", data["queue"]);
    }

    if (data.hasOwnProperty('cluster')) {
        set_cookie("cluster", data["cluster"]);
    }

    if (data.hasOwnProperty('Utilisateur')) {
        set_cookie("users", data["Utilisateur"]);
    }

    if (data.hasOwnProperty('Groupe')) {
        set_cookie("groupe", data["Groupe"]);
    }

    document.getElementById('toutSearch').click();


    document.getElementById("users").value = "";
    document.getElementById("users").click();

    $.getJSON('/who', function (name) {
        $.ajax({
            url: "/output/" + name["user"],
            type: "get",
            data: { outData: "" },
            success: function (response) {
                loadGroups(name["user"]);
            },
            error: function (err) {
                console.log(err)
            }
        });
    });

}

$("#reloadForm").on('click', function (e) {

    if (read_cookie('debut') != null) {
        document.getElementById('periodeSearch').click();
        document.getElementById("dateByForkStart").value = read_cookie('debut');
        document.getElementById("dateByForkEnd").value = read_cookie('fin');

    }

    if (read_cookie('annee') != null) {
        document.getElementById('anneeSearch').click();
        document.getElementById("dateByYear").value = read_cookie('annee');

    }

    if (read_cookie('queue') != null) {
        document.getElementById("queue").value = read_cookie('queue');
    }

    if (read_cookie('cluster') != null) {
        document.getElementById("queue").value = read_cookie('queue');
    }

    if (read_cookie('users') != null) {
        document.getElementById("users").value = read_cookie('users');
        document.getElementById("users").click();
    }

    if (read_cookie('groupe') != null) {
        document.getElementById("groups").value = read_cookie('groupe');
    }
});