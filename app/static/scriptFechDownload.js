async function downloadFile(self) {
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filename: self , type: 'download'}),
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = self;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } else {
            console.error('Error al descargar el archivo:', response.statusText);
        }
    } catch (error) {
        console.error('Error al realizar la solicitud de descarga:', error);
    }
}
