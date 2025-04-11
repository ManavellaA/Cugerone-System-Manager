async function dolar(urls) {
    try {
        const response = await fetch(urls);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.text();
        let num = parseFloat(data.replace(',', '.'));
        num = num.toFixed(2);
        return num.toString().replace('.', ',');
    } catch (error) {
        console.error('Error fetching data: ', error);
    }
}

async function dolar_bill() {
    let dir = "http://192.168.0.201:5010/dolar_billete";
    let data = await dolar(dir);
    let target = document.querySelector('.dolar-billete');
    let text = document.createTextNode(`$ ${data}`);
    target.appendChild(text);
}

dolar_bill();

async function dolar_div() {
    let dir = "http://192.168.0.201:5010/dolar_divisa"
    let data = await dolar(dir);
    let target = document.querySelector('.dolar-divisa');
    let text = document.createTextNode(`$ ${data}`);
    target.appendChild(text);
}
dolar_div()