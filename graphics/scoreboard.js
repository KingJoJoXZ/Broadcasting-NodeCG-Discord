const team1Rep = nodecg.Replicant('team1', {defaultValue: 0});
const team2Rep = nodecg.Replicant('team2', {defaultValue: 0});

const team1E1 = document.getElementById('team1');
const team2E1 = document.getElementById('team2');

team1Rep.on('change', (newVal) => {
    team1E1.innerHTML = newVal;
})

team2Rep.on('change', (newVal) => {
    team2E1.innerHTML = newVal;
})
