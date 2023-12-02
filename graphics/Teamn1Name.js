const name1Rep = nodecg.Replicant('name1');

const name1E1 = document.getElementById('name1');

name1Rep.on('change', (newVal) => {
    name1E1.innerHTML = newVal;
})
