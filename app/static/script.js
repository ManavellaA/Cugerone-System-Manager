const table = document.getElementById('dataTable');
const searchInput = document.getElementById('searchInput');
let data = [];
let order = [];

function flaskOrder(vars) {
    order = vars;
}

function flaskData(vars) {
    data = vars;
}

document.addEventListener("DOMContentLoaded", function () {
    let follow_up = document.getElementById("titlePage").textContent;

    function orderData(data) {
        return data.map(item => {
            let orderedItem = {};
            order.forEach(key => {
                orderedItem[key] = item[key] || '';
            });
            return orderedItem;
        });
    }

    function generateTableHead(table, data) {
        let thead = table.createTHead();
        let row = thead.insertRow();
        row.classList.add('text-center');

        Object.keys(data[0]).forEach(key => {
            let th = document.createElement("th");
            let text = document.createTextNode(key);
            th.appendChild(text);
            th.classList.add('filter-header');
            th.setAttribute('data-key', key);
            row.appendChild(th);

            let filterContainer = document.createElement("div");
            filterContainer.classList.add('filter-container');
            filterContainer.setAttribute('data-key', key);
            
            let select = document.createElement("select");
            let uniqueValues = [...new Set(data.map(item => item[key]))].sort();

            let defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.text = `Filtrar por ${key}`;
            select.appendChild(defaultOption);

            uniqueValues.forEach(value => {
                let option = document.createElement("option");
                option.value = value;
                option.text = value;
                select.appendChild(option);
            });

            select.addEventListener('change', filterTableByColumns);

            filterContainer.appendChild(select);
            th.appendChild(filterContainer);
        });
    }

    function generateTable(table, data) {
        let tbody = table.getElementsByTagName('tbody')[0];
        tbody.innerHTML = ""; // Limpiar filas existentes
    
        data.forEach(element => {
            let row = tbody.insertRow();
            row.classList.add('text-center');
            order.forEach(key => {
                let cell = row.insertCell();
                cell.setAttribute("style", "border: grey 1px solid;");
    
                if (key === "Numero") {
                let link = document.createElement('a');
                link.href = `#`;
                    link.textContent = element[key] || '';
                    cell.appendChild(link);
                    link.onclick = function() {
                        window.open(`/view/${element["Numero"]}`, '_blank');
                    };
                } 
                else if (key === "Estado") {
                    let tipe = {}; 
                    if (follow_up === "Seguimiento de OC") {
                        tipe = {Aceptado: "Entregado", Rechazado: "Anulado", Parcial: "Editado"};
                    }
                    else if (follow_up === "Seguimiento de Presupuestos") {
                        tipe = {Aceptado: "Aceptado", Rechazado: "Rechazado", Parcial: "Parcial"};
                    }
                    if (element["Estado"] === tipe.Aceptado || element["Estado"] === "Aceptado" || element["Estado"] === tipe.Rechazado || element["Estado"] === tipe.Parcial) {
                        if (element["Estado"] === "Aceptado" && follow_up === "Seguimiento de OC"){
                            element["Estado"] = "Entregado";
                        }
                        cell.textContent = element["Estado"];
    
                        let auxiliaryButton = document.createElement('button');
                        auxiliaryButton.textContent = "X";
                        auxiliaryButton.classList.add('btn', 'btn-danger', 'ml-1', 'ms-3');
                        auxiliaryButton.onclick = function() {
                            element["Estado"] = "";
                            actualizarEstado(element["Numero"], "");
                            generateTable(table, data)
                        };
                        cell.appendChild(auxiliaryButton);
                    } else {
                        let acceptButton = document.createElement('button');
                        let denyButton = document.createElement('button');
                        let partialButton = document.createElement('button');
                        acceptButton.textContent = tipe.Aceptado;
                        denyButton.textContent = tipe.Rechazado;
                        partialButton.textContent = tipe.Parcial;
                        acceptButton.classList.add('btn', 'btn-success', 'ml-1', 'me-1');
                        denyButton.classList.add('btn', 'btn-danger', 'ml-1', 'me-1');
                        partialButton.classList.add('btn', 'btn-secondary', 'ml-1');
                        acceptButton.onclick = function() {
                            element["Estado"] = tipe.Aceptado;
                            actualizarEstado(element["Numero"], tipe.Aceptado);
                            generateTable(table, data);
                        };
                        
                        denyButton.onclick = function() {
                            element["Estado"] = tipe.Rechazado;
                            actualizarEstado(element["Numero"], tipe.Rechazado);
                            generateTable(table, data);
                        };

                        partialButton.onclick = function() {
                            window.location.href = `/edit/${element["Numero"]}`;
                            generateTable(table, data);
                        };
                        
                        cell.appendChild(acceptButton);
                        cell.appendChild(denyButton);
                        cell.appendChild(partialButton);
                    }
                } 

                else if (key === "Estado_pago") {
                    tipe = {Aceptado: "Pagado", Rechazado: "Anulado", Parcial: "Agendado"};


                    if (element["Estado_pago"] == tipe.Aceptado || element["Estado_pago"] == tipe.Rechazado || element["Estado_pago"] == tipe.Parcial) {
                        cell.textContent = element["Estado_pago"];
                        if (cell.textContent == tipe.Aceptado){
                            cell.setAttribute("style", "color: green; font-weight: bold; border: grey 1px solid; font-size: 1.4vh;");
                        } else if (cell.textContent == tipe.Rechazado){
                            cell.setAttribute("style", "color: red; font-weight: bold; border: grey 1px solid; font-size: 1.4vh;");
                        } else {
                            cell.setAttribute("style", "color: orange; font-weight: bold; border: grey 1px solid; font-size: 1.4vh;")
                        }
                        let auxiliaryButton = document.createElement('button');
                        auxiliaryButton.textContent = "X";
                        auxiliaryButton.classList.add('btn', 'btn-danger', 'ml-1', 'ms-3');
                        auxiliaryButton.setAttribute("style", "font-size: 1.2vh;");
                        auxiliaryButton.onclick = function() {
                            element["Estado_pago"] = "";
                            actualizarEstadoPago(element["Numero"], "");
                            generateTable(table, data);
                        };
                        cell.appendChild(auxiliaryButton);
                    } else {
                        let acceptButton = document.createElement('button');
                        let denyButton = document.createElement('button');
                        let partialButton = document.createElement('button');
                        acceptButton.textContent = tipe.Aceptado;
                        denyButton.textContent = tipe.Rechazado;
                        partialButton.textContent = tipe.Parcial;
                        acceptButton.classList.add('btn', 'btn-success', 'ml-1', 'me-1');
                        acceptButton.setAttribute("style", "font-size: 1.2vh;");
                        denyButton.classList.add('btn', 'btn-danger', 'ml-1', 'me-1');
                        denyButton.setAttribute("style", "font-size: 1.2vh;");
                        partialButton.classList.add('btn', 'btn-secondary', 'ml-1');
                        partialButton.setAttribute("style", "font-size: 1.2vh;");
                        
                        acceptButton.onclick = function() {
                            element["Estado_pago"] = tipe.Aceptado;
                            actualizarEstadoPago(element["Numero"], tipe.Aceptado);
                            generateTable(table, data);
                        };
                        
                        denyButton.onclick = function() {
                            element["Estado_pago"] = tipe.Rechazado;
                            actualizarEstadoPago(element["Numero"], tipe.Rechazado);
                            generateTable(table, data);
                        };

                        partialButton.onclick = function() {
                            element["Estado_pago"] = tipe.Parcial;
                            actualizarEstadoPago(element["Numero"], tipe.Parcial);
                            generateTable(table, data);
                        };
                        
                        cell.appendChild(acceptButton);
                        cell.appendChild(denyButton);
                        cell.appendChild(partialButton);
                    }
                    
                }
                
                else if (key === "Comprobante") {
                    let auxiliaryC = document.createElement('button');
                    let auxiliaryI = document.createElement('input');
                    auxiliaryI.setAttribute("type","file")
                    auxiliaryI.setAttribute("style","display: none;")
                    if (element["Comprobante"] !== ""){
                        auxiliaryC.textContent = 'Descargar';
                        auxiliaryC.classList.add('btn', 'btn-success', 'ml-1', 'me-1');
                        auxiliaryC.onclick = function() {
                            const num = element["Numero"]
                            downloadFile(num, 'adm')
                        };
                    }
                    else{
                        auxiliaryC.textContent = "Subir";
                        auxiliaryC.classList.add('btn', 'btn-primary', 'ml-1', 'me-1');
                        auxiliaryC.onclick = function() { auxiliaryI.click() };
                        auxiliaryI.addEventListener("change" ,handleFiles);
                        function handleFiles(event) {
                            event.preventDefault();
                            const files = event.target.files;
                            if (files.length > 0) {
                                const file = files[0];
                                const num = element["Numero"]
                                uploadFile(file, num, 'comp');
                            }
                        generateTable(table, data)
                        }
                    }
                    cell.appendChild(auxiliaryC)
                }

                else if (key === "Fecha_de_pago") {
                    let change_date_pay = document.createElement('input')
                    change_date_pay.setAttribute("type","date")
                    let view_date_pay = document.createElement('a')
                    view_date_pay.setAttribute("style","display: block; text-decoration: underline;")
                    view_date_pay.textContent = element['Fecha_de_pago']
                    cell.appendChild(view_date_pay)
                    view_date_pay.onclick = function() {
                        cell.appendChild(change_date_pay)
                        change_date_pay.addEventListener('change', handlerChange)
                        function handlerChange(e) {
                            e.preventDefault
                            let date = change_date_pay.value
                            let num = element['Numero']
                            fetch_changue_pay(date, num)
                        }
                    }
                }

                else if (key === "FC") {
                    let auxiliaryFC = document.createElement('button');
                    let auxiliaryA = document.createElement('input');
                    auxiliaryA.setAttribute("type","file")
                    auxiliaryA.setAttribute("style","display: none;")
                    if (element["FC"] !== ""){
                        auxiliaryFC.textContent = 'Descargar';
                        auxiliaryFC.classList.add('btn', 'btn-success', 'ml-1', 'me-1');
                        auxiliaryFC.onclick = function() {
                            const num = element["Numero"]
                            downloadFile(num, 'fc')
                        };
                    }
                    else{
                        auxiliaryFC.textContent = "Subir";
                        auxiliaryFC.classList.add('btn', 'btn-primary', 'ml-1', 'me-1');
                        auxiliaryFC.onclick = function() { auxiliaryA.click() };
                        auxiliaryA.addEventListener("change" ,handleFiles);
                        function handleFiles(event) {
                            event.preventDefault();
                            const files = event.target.files;
                            if (files.length > 0) {
                                const file = files[0];
                                const num = element["Numero"]
                                uploadFile(file, num, 'fc');
                            }
                            generateTable(table, data)
                        }
                    }
                    cell.appendChild(auxiliaryFC)
                }

                else {
                    cell.textContent = element[key] || '';
                }
            
            });
        });
    }

    function actualizarEstado(numero, nuevoEstado) {
        let dolar_b = document.querySelector('.dolar-billete').textContent;
        let dolar_d = document.querySelector('.dolar-divisa').textContent;
        fetch('/guardar-estado', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ Numero: numero, Estado: nuevoEstado, DolarBillete: dolar_b, DolarDivisa: dolar_d, ref: follow_up }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la actualización del estado');
            }
            return response.json();
        })
        .then(data => {
            console.log('Estado Actualizado');
        })
        .catch(error => {
            console.error('Error al actualizar el estado:', error);
        });
    }

    function actualizarEstadoPago(numero, estado_pay) {
        fetch('/guardar-estado', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ Numero: numero, Estado_pago: estado_pay, ref: follow_up }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la actualización del estado');
            }
            return response.json();
        })
        .then(data => {
            console.log('Estado Actualizado');
        })
        .catch(error => {
            console.error('Error al actualizar el estado:', error);
        });
    }

    function uploadFile(file, num, type) { 
        const formData = new FormData();
        formData.append("file", file);
        formData.append("num", num);
        formData.append("type", type);
    
        fetch("/upload/adm", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else if (data.json_path) {
                alert("Archivo " + data.json_path + " subido con éxito");
                location.reload()
            } else {
                alert("Archivo subido pero sin ruta en la respuesta.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error al subir el archivo.");
        });
    }

    function fetch_changue_pay(date, num){
        fetch('/guardar-estado', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ Fecha: date, Numero: num, ref: 'fecha' }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la actualización de fecha');
            }
            return response.json();
        })
        .then(data => {
            alert('Fecha Actualizada');
            location.reload()
        })
        .catch(error => {
            console.error('Error al actualizar el estado:', error);
        });
    }

    async function downloadFile(self, type) {
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ filename: self , type: type}),
            });
    
            if (response.ok) {
                const disposition = response.headers.get('Content-Disposition');
                let filename = 'archivo_descargado';
                if (disposition && disposition.includes('filename=')) {
                    const match = disposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                    if (match && match[1]) {filename = match[1].replace(/['"]/g, '');}
                }
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename; 
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            } else {
                console.error('Error al descargar el archivo:', response.statusText);
            }
        } catch (error) {
            console.error('Error al realizar la solicitud de descarga:', error);
        }
    }
    

    function searchTable(query) {
        const filteredData = data.filter(item =>
            Object.values(item).some(val =>
                String(val).toLowerCase().includes(query)
            )
        );

        if (filteredData.length === 0) {
            const toast = document.querySelector('.toast');
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 2000);
        } else {
            generateTable(table, filteredData);
        }
    }

    function filterTableByColumns() {
        let filters = {};
        document.querySelectorAll('.filter-container select').forEach(select => {
            let key = select.closest('.filter-container').getAttribute('data-key');
            let value = select.value.toLowerCase();
            if (value) {
                filters[key] = value;
            }
        });

        const filteredData = data.filter(item => {
            return Object.keys(filters).every(key => {
                return String(item[key]).toLowerCase().includes(filters[key]);
            });
        });

        generateTable(table, filteredData);
    }

    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            const query = searchInput.value.toLowerCase();
            searchTable(query);
        }
    });

    document.querySelectorAll('.filter-header').forEach(header => {
        header.addEventListener('mouseover', () => {
            const key = header.getAttribute('data-key');
            document.querySelectorAll('.filter-container').forEach(container => {
                if (container.getAttribute('data-key') === key) {
                    container.classList.add('show');
                }
            });
        });

        header.addEventListener('mouseout', () => {
            const key = header.getAttribute('data-key');
            document.querySelectorAll('.filter-container').forEach(container => {
                if (container.getAttribute('data-key') === key) {
                    container.classList.remove('show');
                }
            });
        });
    });

    if (data.length > 0 && order.length > 0) {
        let orderedData = orderData(data);
        generateTableHead(table, orderedData);
        generateTable(table, orderedData);
    }
});
