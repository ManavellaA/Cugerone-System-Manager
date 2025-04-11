document.addEventListener("DOMContentLoaded", function () {

    const uploadContainer = document.getElementById("upload-container");
    const fileInput = document.getElementById("fileInput");


    uploadContainer.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener("change", handleFiles);

    uploadContainer.addEventListener("dragover", (event) => {
        event.preventDefault();
        uploadContainer.classList.add("dragover");
    });

    uploadContainer.addEventListener("dragleave", () => {
        uploadContainer.classList.remove("dragover");
    });

    uploadContainer.addEventListener("drop", (event) => {
        event.preventDefault();
        uploadContainer.classList.remove("dragover");
        const files = event.dataTransfer.files;
        handleFiles({ target: { files: files } });
    });

    function handleFiles(event) {
        const files = event.target.files;
        if (files.length > 0) {
            const file = files[0];
            uploadFile(file);
        }
    }

    function uploadFile(file) {
        const formData = new FormData();
        document.getElementsByClassName("upload")[0].hidden = true;
        document.getElementsByClassName("chargue")[0].hidden = false;
        formData.append("file", file);

        console.log(formData);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementsByClassName("upload")[0].hidden = false;
                    document.getElementsByClassName("chargue")[0].hidden = true;
                    alert("Error: " + data.error);
                } else {
                    document.getElementsByClassName("upload")[0].hidden = false;
                    document.getElementsByClassName("chargue")[0].hidden = true;
                    alert("Archivo " + data.json_path + " subido con éxito");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                document.getElementsByClassName("upload")[0].hidden = false;
                document.getElementsByClassName("chargue")[0].hidden = true;
                alert("Error al subir el archivo.");
            });
    }
})