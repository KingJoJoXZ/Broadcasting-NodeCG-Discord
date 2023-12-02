
const nameElement = document.getElementById('name');
const titleElement = document.getElementById('title');

// You can use NodeCG messages to update the content dynamically.
nodecg.listenFor('updateLowerThird', (data) => {
    nameElement.innerText = data.name;
    titleElement.innerText = data.title;
});
