const name2Rep =  nodecg.Replicant('name2');

function updateNames(){
    nodecg.listenFor('updateTeamNames2', (data) => {
        teamReplicant.value = data;
    })
}