function formsetup(data) {


    if(data.hasOwnProperty('Année')){
        document.getElementById('anneeSearch').click();
    }

    if(data.hasOwnProperty('Debut')){
        document.getElementById('periodeSearch').click();
    }

    if(data.hasOwnProperty('queue')){
        document.getElementById("queue").value = data["queue"];
        document.getElementById('queueSearch').click();
    }

    if(data.hasOwnProperty('cluster')){
        document.getElementById("cluster").value = data["cluster"];
        document.getElementById('clusterSearch').click();
    }
    
}

