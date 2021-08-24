/**
 * @author Damien LE BORGNE
 */

function loadGroups(name){

    $.getJSON('/output/'+name, function(data, status, xhr){

        var options = '<option value="Tout">Tout</option>';
        
        for (var i = 0; i < data["groupes"].length; i++ ) {
            options += '<option value="' + data["groupes"][i]+ '" '+select+'>' + data["groupes"][i] + '</option>';
            select = "";
        }
        // console.log(data["groupes"]);
        $("#groups").html(options);  
    });
}

function loadLists(){
    
    var listUsers = [];

//  Ajouter tout les utilisateurs de la bdd dans un array retourner la liste sous format json dans /users (python), Recuperer la liste et le push dans listUsers (js)
    $.getJSON('/users', function(data){
     for (var i = 0; i < data["users"].length; i++ ) {
        listUsers.push(data["users"][i]);
     }
    });

//  Charger les groupes dans un select
    $.getJSON('/who', function(name){
        loadGroups(name["user"]);
    });

//  Charger les queues dans un select
    $.getJSON('/queues', function(data, status, xhr){
        var options = '<option value="Aucune" selected>Aucune</option>';
        options += '<option value="Tout">Tout</option>';
        for (var i = 0; i < data["queues"].length; i++ ) {
            options += '<option value="' + data["queues"][i]+ '">' + data["queues"][i] + '</option>';
            select = "";
        }
        // console.log(data["groupes"]);
        $("#queue").html(options);  
    });

//  Charger les clusters dans un select
    $.getJSON('/clusters', function(data, status, xhr){
        options = '<option value="Aucune" selected>Aucune</option>';
        for (var i = 0; i < data["clusters"].length; i++ ) {
            options += '<option value="' + data["clusters"][i]+ '">' + data["clusters"][i] + '</option>';
        }
        // console.log(data["groupes"]);
        $("#cluster").html(options);  
    });

// Autocompletion
   $( "#users" ).autocomplete({
    source: function( request, response ) {
            var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
            response( $.grep( listUsers, function( item ){
                return matcher.test( item );
            }) );
        }
    });
};

$(document).ready(function(){

    loadLists();

//  Recuperer l'id de l'utilisateur dans /who puis pour chaque Keyup, retourner l'input /output/id Flask retournera une reponse
    $.getJSON('/who', function(name){
        $("#users").keyup(function(){
            var text = $(this).val();
            $.ajax({
              url: "/output/"+name["user"],
              type: "get",
              data: {outData: text},
              success: function(response) {
                loadGroups(name["user"]);
              },
              error: function(err) {
                console.log(err)
              }
            });
        });

        $( "#users" ).on( "click", function() {
            var text = $(this).val();
            $.ajax({
              url: "/output/"+name["user"],
              type: "get",
              data: {outData: text},
              success: function(response) {
                loadGroups(name["user"]);
              },
              error: function(err) {
                console.log(err)
              }
            });
        });
    });

    
    
    $("button").on('click', function(e) {
        e.preventDefault();
    });

    $("input#reset").on('click', function(e) {
        document.getElementById("users").value = ""; 
    });

//  Eviter la frappe entrée lorsque l'utilisateur entre un nom (eviter de valider le formulaire)
    $(window).keydown(function(event){
        if(event.keyCode == 13) {
          event.preventDefault();
          return false;
        }
      });
   
});