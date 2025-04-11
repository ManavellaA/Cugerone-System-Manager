let empresas = []
let tipo = document.getElementById('title').textContent;
console.log(tipo)

function flaskdata(vars) {
    empresas = vars;
}

document.getElementById('selectCliente').addEventListener('change', function () {
    let selectedValue = this.value;
    let datosClienteDiv = document.getElementById('datosCliente');
    let btnGuardar = document.getElementById('btnGuardar');
    if (selectedValue == 'new') {
        document.getElementById('inputNombre').style.display = 'block';
        datosClienteDiv.style.display = 'block';
        btnGuardar.style.display = 'flex';
        clearInputs();
    } else if (selectedValue) {
        let empresaSeleccionada = empresas.find(e => e.nombre === selectedValue);
        if (empresaSeleccionada) {
            document.getElementById('inputNombre').value = empresaSeleccionada.nombre;
            document.getElementById('inputCUIT').value = empresaSeleccionada.cuit;
            if (tipo == "Datos Cliente") {
                document.getElementById('selectIVA').value = empresaSeleccionada.iva;
            }
            if (tipo == "Datos Proveedor") {
                document.getElementById('inputDireccion').value = empresaSeleccionada.direccion;
            }
            document.getElementById('inputCiudad').value = empresaSeleccionada.ciudad;
            document.getElementById('inputCP').value = empresaSeleccionada.cp;
            document.getElementById('inputNombre').style.display = 'none';
            datosClienteDiv.style.display = 'block';
            btnGuardar.style.display = 'flex';
        }
    } else {
        document.getElementById('inputNombreCliente').style.display = 'block';
        datosClienteDiv.style.display = 'none';
        btnGuardar.style.display = 'none';
        clearInputs();
    }
});

function clearInputs() {
    document.getElementById('inputNombre').value = '';
    document.getElementById('inputCUIT').value = '';
    if (tipo === "Datos Cliente") {
    document.getElementById('selectIVA').value = '';
    }
    if (tipo === "Datos Proveedor") {
        document.getElementById('inputDireccion').value = '';
    }
    document.getElementById('inputCiudad').value = '';
    document.getElementById('inputCP').value = '';
}

// Definir las funciones globalmente para que estén accesibles desde cualquier lugar

function addRow() {
    let table = document.getElementById('inputTable').getElementsByTagName('tbody')[0];
    let newRow = table.insertRow();

    for (let i = 0; i < 4; i++) {
        let newCell = newRow.insertCell();
        let input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control form-control-sm';
        newCell.appendChild(input);
    }
}

function getFormData() {
    // Obtener datos
    let entry = {}

    if (tipo == "Datos Proveedor") {
        entry = {
            nombre: document.getElementById('inputNombre').value,
            cuit: document.getElementById('inputCUIT').value,
            direccion: document.getElementById('inputDireccion').value,
            ciudad: document.getElementById('inputCiudad').value,
            cp: document.getElementById('inputCP').value,
        };
    }
    else if (tipo == "Datos Cliente") {
        entry = {
            nombre: document.getElementById('inputNombre').value,
            cuit: document.getElementById('inputCUIT').value,
            iva: document.getElementById('selectIVA').value,
            ciudad: document.getElementById('inputCiudad').value,
            cp: document.getElementById('inputCP').value,
        };
    }
    // Obtener artículos de la tabla dinámica
    let articulos = [];
    let rows = document.querySelectorAll('#inputTable tbody tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('input');
        if (cells[0].value !== '') {
            articulos.push({
                articulo: cells[0].value,
                cantidad: cells[1].value,
                unitario: cells[2].value,
                observaciones: cells[3].value
            });}
    });

    // Obtener condiciones comerciales
    let condicionesComerciales = [];
    document.querySelectorAll('#panelsStayOpen-collapseThree input[type="text"]').forEach(input => {
        condicionesComerciales.push(input.value);
    });

    let otros = [];
    if (document.getElementById('otros').value.length > 0) {
        data = document.getElementById('otros').value;
        otros.push(data);
    } else {
        data = 'No hay observaciones.';
        otros.push(data);
    }
    
    let date = ''
    let method_pay = ''
    let day_pay = ''
    if (tipo == "Datos Proveedor") {
        date = document.getElementById('date').value;
        method_pay = document.getElementById('method-pay').value;
        day_pay = document.getElementById('day-pay').value;
    }
    let firma = document.getElementById('firma').value;
    let moneda_type = document.getElementById('moneda').value;
    let moneda = '$';
    if (moneda_type == 'U$DD' || moneda_type == 'U$DB') {
        moneda = 'U$D';
    }

    formData = {}

    // Crear el objeto final
    if (tipo == "Datos Proveedor") {
        formData = {
            proveedor: entry,
            articulos: articulos,
            condiciones: {
                comerciales: condicionesComerciales,
                otros: otros
            },
            firma: firma,
            moneda: moneda,
            moneda_tipo: moneda_type,
            fecha: date,
            forma_pago: method_pay,
            fecha_pago: day_pay,
            estado_pago:'',
            tipe: tipo,
        };
    }
    else if (tipo == "Datos Cliente") {
        formData = {
            cliente: entry,
            articulos: articulos,
            condiciones: {
                comerciales: condicionesComerciales,
                otros: otros
            },
            firma: firma,
            moneda: moneda,
            moneda_tipo: moneda_type,
            tipe: tipo
        };
    }

    return formData;
}

function enviarDatos() {
    if (tipo == "Datos Proveedor") {    
        if (document.getElementById('firma').value == '' || document.getElementById('date').value == '') {
            return alert('Firma y Fecha de Entrega son estrictamente Requeridos.');
        }
    }
    else if (document.getElementById('firma').value == '') {
        return alert('Ingrese el nombre de quien firma el presupuesto.');
    }

        const data = getFormData();

        if (tipo == "Datos Proveedor") {
            fetch('/upstream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                if (result.number) {

                    window.open(`/view/${result.number}`, '_blank');

                    window.location.href = `/list/Supplier`;

                } else {
                    alert('Error al guardar.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al guardar.');
            });
        }

        else if (tipo == "Datos Cliente") {
            fetch('/upstream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(result => {
                if (result.number) {

                    window.open(`/view/${result.number}`, '_blank');

                    window.location.href = `/list/Client`;

                } else {
                    alert('Error al guardar.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al guardar.');
            });
        }
    }


// Este evento solo afecta a la lógica de guardar un cliente
document.getElementById('btnGuardar').addEventListener('click', function () {
    if (tipo == "Datos Cliente") {
        const cliente = {
            nombre: document.getElementById('inputNombre').value,
            cuit: document.getElementById('inputCUIT').value,
            iva: document.getElementById('selectIVA').value,
            ciudad: document.getElementById('inputCiudad').value,
            cp: document.getElementById('inputCP').value
        };

        fetch('/guardar/<client>', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cliente)
        }).then(response => {
            if (response.ok) {
                alert('Guardado con éxito.');
            } else {
                alert('Error al guardar.');
            }
        });
    }
    else if (tipo == "Datos Proveedor") {
        
        const proveerdor = {
            nombre: document.getElementById('inputNombre').value,
            cuit: document.getElementById('inputCUIT').value,
            ciudad: document.getElementById('inputCiudad').value,
            direccion: document.getElementById('inputDireccion').value,
            cp: document.getElementById('inputCP').value
        };

        fetch('/guardar/<supplier>', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(proveerdor)
        }).then(response => {
            if (response.ok) {
                alert('Guardado con éxito.');
            } else {
                alert('Error al guardar.');
            }
        });
    }
    
});
