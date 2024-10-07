const singleInputs = document.querySelectorAll(".input-container > input.form-control-file:not([multiple])");
singleInputs.forEach(
    function (singleInput) {
        singleInput.addEventListener(
            "change",
            function () {
                const fileName = singleInput.value.split('\\').pop();
                singleInput.parentElement.querySelector("label.file-upload-label")
                    .textContent = fileName || "Выбрать файл";
            }
        );
    }
)

const multiInputs = document.querySelectorAll(".input-container > input.form-control-file[multiple]");
multiInputs.forEach(
    function (multiInput) {
        multiInput.addEventListener(
            "change",
            function () {
                const fileList = multiInput.files;
                const countFiles = fileList.length
                document.querySelector('label.file-upload-label').textContent =
                    countFiles === 0
                        ? "Выбрать файлы"
                        : "Выбрано файлов: " + countFiles;
            }
        );
    }
)
