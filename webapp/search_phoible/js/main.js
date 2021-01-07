const REQUEST_URL = 'https://eurphon.info/query/query';
// const REQUEST_URL = 'http://127.0.0.1:11000/query/query';

const colourClasses = [
    'circle-6f6456',
    'circle-cddc49',
    'circle-cb7e94',
    'circle-e94b30',
    'circle-fee659',
    'circle-a1cfdd',
    'circle-fdbab4',
    'circle-0cea20',
    'circle-7dd97d',
    'circle-bcddf7',
    'circle-f4c674',
    'circle-adf875',
    'circle-f4d11e',
    'circle-c397ca',
    'circle-e2f982',
    'circle-f6e39c',
    'circle-dd93e1',
    'circle-26f5cc',
    'circle-f04b50',
    'circle-005350',
    'circle-15a67d',
    'circle-a0f535',
    'circle-acf9b4'
];

let allPhyla = {},
    map,
    mapMarkers = [];

function byId(id) {
    return document.getElementById(id);
}

async function submitQuery() {
    byId('waiting-span').style.display = 'inline-block';

    const queryString = byId('query-string').value;
    if (queryString.length === 0)
        return;
    const response = await fetch(REQUEST_URL, {
        method: 'POST',
        body: JSON.stringify({
            'query_string': queryString,
            'phoible': true
        })
    });

    byId('waiting-span').style.display = 'none';
    byId('done-span').style.display = 'inline-block';
    setTimeout(() => { byId('done-span').style.display = 'none'; }, 500);

    if (!response.ok) {
        const error = await response.text();
        alert(`Error: ${error}`);
        return;
    }
    const data = await response.json();
    let nLangs = 0;
    for (const key in data)
        if (data.hasOwnProperty(key))
            nLangs++;

    drawMap(data);
    populateTable(data);
}

function drawMap(data) {
    allPhyla = {};
    let nPhyla = 0;

    // Delete old markers from the map.
    for (const marker of mapMarkers)
        map.removeLayer(marker);
    mapMarkers.length = 0;

    for (const key in data) {
        if (!data.hasOwnProperty(key))
            continue;

        // const phylum = data[key].phylum;
        // let colourIndex;
        // if (allPhyla.hasOwnProperty(phylum))
        //     colourIndex = allPhyla[phylum];
        // else {
        //     colourIndex = nPhyla;
        //     allPhyla[phylum] = nPhyla;
        //     nPhyla++;
        // }

        // Add map markers
        try {
            const latitude = parseFloat(data[key].latitude),
                longitude = parseFloat(data[key].longitude);
            let circle = L.divIcon({
                className: 'circle ' + 'circle-red',
                iconSize: [10, 10]
            });
            let marker = L.marker([latitude, longitude], {
                icon: circle,
                title: data[key].name
            });

            marker.on('click', () => {
                window.open(`https://phoible.org/inventories/view/${key}`)
            });

            mapMarkers.push(marker);
            marker.addTo(map);
        } catch {
            ;
        }
    }
    console.log(nPhyla);
}

function populateTable(data) {
    let container = byId('table');
    container.innerHTML = '';
    let tableData = data2Rows(data);

    const nLangs = tableData.length;
    byId('n-langs').innerText = nLangs === 0 ?
        'No languages found' :
        (nLangs === 1 ?
            '1 language found:' :
            `${nLangs} languages found:`);
    byId('n-langs').style.display = 'inline-block';
    byId('n-langs').style['margin-bottom'] = '20px';

    let _ = new Handsontable(container, {
        licenseKey: 'non-commercial-and-evaluation',
        data: data2Rows(data),
        colHeaders: ['Language', 'Glottocode', 'Phylum', 'Genus'],
        editor: false,
        rowHeaders: false,
        filters: true,
        dropdownMenu: [
            'filter_by_condition',
            'filter_by_value',
            'filter_action_bar'
        ],
        columns: [
            { data: 'name', renderer: 'html' },
            { data: 'glottocode' },
            { data: 'phylum' },
            { data: 'genus' }
        ],
        columnSorting: true
    });
}

// TODO: update the code to use different shapes in addition
// to colours.
function phylumRenderer(instance, td, row, col, prop, value, cellProperties) {
    while (td.firstChild) {
        td.removeChild(td.firstChild);
    }
    td.append(document.createTextNode(value + ' '));

    let circle = document.createElement('div');
    circle.style.display = 'inline-block';
    circle.classList.add('circle');
    circle.classList.add(colourClasses[allPhyla[value]]);
    td.append(circle);
}


function data2Rows(data) {
    let rows = [];
    for (const key in data) {
        if (!data.hasOwnProperty(key))
            continue;
        const val = data[key];
        rows.push({
            name: `${val.name} <a href="https://phoible.org/inventories/view/${key}" target="_blank">🔗</a>`,
            glottocode: val.glottocode,
            phylum: val.phylum,
            genus: val.genus
        });
    }
    rows.sort((r1, r2) => {
        if (r1.name < r2.name)
            return -1;
        else if (r1.name > r2.name)
            return 1;
        else
            return 0;
    })
    return rows;
}

document.addEventListener('DOMContentLoaded', () => {
    map = L.map('map', { zoomControl: false });
    map.setView([40, 20], 2);
    L.control.zoom({ position: 'bottomleft' }).addTo(map);
    L.tileLayer(
        'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            maxZoom: 18,
        })
        .addTo(map);
});