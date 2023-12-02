const name2Rep = nodecg.Replicant('name2');

const name2E1 = document.getElementById('name2');

name2Rep.on('change', (newVal) => {
    name2E1.innerHTML = newVal;
})