// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', () => {
  // Get the input and output elements
  const userInput = document.getElementById('userInput');
  const botOutput = document.getElementById('botOutput');
  const csvFileInput = document.getElementById('csvFile');
  const uploadForm = document.getElementById('uploadForm');
  const datasetContainer = document.getElementById('dataset');
  const uploadButton = document.getElementById('uploadButton');

  // Function to handle the upload and process the CSV file
  const handleUpload = () => {
    const formData = new FormData();
    formData.append('csv_file', csvFileInput.files[0]);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(textData => {
        datasetContainer.textContent = textData;
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };


  uploadButton.addEventListener('click', handleUpload);


  // Function to handle the chat interaction
  const handleChat = () => {
    const formData = new FormData();
    formData.append('user_input', userInput.value);

    fetch('/chat', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        botOutput.value = data.bot_response;
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  // Add an event listener to the user input element
  userInput.addEventListener('keypress', event => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleChat();
    }
  });

  // Add an event listener to the form submit button
  uploadForm.addEventListener('submit', event => {
    event.preventDefault();
    handleUpload();
  });
});
