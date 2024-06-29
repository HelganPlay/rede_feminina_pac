const uploadBox = document.getElementById('upload-box');

      uploadBox.addEventListener('click', () => {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);
        fileInput.click();

        fileInput.onchange = () => {
          const file = fileInput.files[0];
          if (file) {
            uploadFile(file);
          }
        };
      });

      uploadBox.addEventListener('dragover', (event) => {
        event.preventDefault();
        event.stopPropagation();
        uploadBox.style.backgroundColor = '#f1f1f1';
      });

      uploadBox.addEventListener('dragleave', (event) => {
        event.preventDefault();
        event.stopPropagation();
        uploadBox.style.backgroundColor = '#fff';
      });

      uploadBox.addEventListener('drop', (event) => {
        event.preventDefault();
        event.stopPropagation();
        uploadBox.style.backgroundColor = '#fff';

        const file = event.dataTransfer.files[0];
        if (file) {
          uploadFile(file);
        }
      });

      function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
          method: 'POST',
          body: formData,
        })
        .then(data => {

      // Redireciona para a rota '/' apenas após o processamento da resposta
      window.location.href = '/';
        })}