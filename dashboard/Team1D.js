const name1Rep =  nodecg.Replicant('name1');

function updateNames(){
    nodecg.listenFor('updateTeamNames', (data) => {
        teamReplicant.value = data;
    })
}
