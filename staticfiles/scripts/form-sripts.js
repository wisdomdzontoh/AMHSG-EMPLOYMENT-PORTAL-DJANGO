function showSection(sectionNumber) {
  // Hide all sections
  const sections = document.querySelectorAll('[id^="section-"]');
  sections.forEach((section) => section.classList.add("hidden"));

  // Show selected section
  document
    .getElementById(`section-${sectionNumber}`)
    .classList.remove("hidden");

  // Reset all steps to inactive
  const steps = document.querySelectorAll('[id^="step-"]');
  steps.forEach((step) => {
    step.classList.remove("bg-indigo-100", "text-indigo-700");
    step
      .querySelector("span")
      .classList.replace("bg-indigo-500", "bg-gray-300");
    step.querySelector("span").classList.replace("text-white", "text-gray-700");
  });

  // Activate the selected step
  const selectedStep = document.getElementById(`step-${sectionNumber}`);
  selectedStep.classList.add("bg-indigo-100", "text-indigo-700");
  selectedStep
    .querySelector("span")
    .classList.replace("bg-gray-300", "bg-indigo-500");
  selectedStep
    .querySelector("span")
    .classList.replace("text-gray-700", "text-white");
}

// Drag and Drop with Image Preview
const dropArea = document.getElementById("image-drop-area");
const input = document.getElementById("image-upload");
const previewContainer = document.getElementById("image-preview");

dropArea.addEventListener("click", () => {
  input.click();
});

dropArea.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropArea.classList.add("border-indigo-500");
});

dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("border-indigo-500");
});

dropArea.addEventListener("drop", (event) => {
  event.preventDefault();
  dropArea.classList.remove("border-indigo-500");

  const file = event.dataTransfer.files[0];
  handleFile(file);
});

input.addEventListener("change", (event) => {
  const file = event.target.files[0];
  handleFile(file);
});

function handleFile(file) {
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = (event) => {
      const img = document.createElement("img");
      img.src = event.target.result;
      img.classList.add("w-full", "h-full", "object-cover", "rounded-lg");
      previewContainer.innerHTML = ""; // Clear existing content
      previewContainer.appendChild(img); // Add the image preview
    };
    reader.readAsDataURL(file);
  } else {
    alert("Please upload an image file.");
  }
}

// Initialize flatpickr for date fields
document.addEventListener("DOMContentLoaded", function () {
  flatpickr("#date-started", {
    dateFormat: "d/m/Y",
  });
  flatpickr("#date-completed", {
    dateFormat: "d/m/Y",
  });
});

function addEducationalBackground() {
  // Get values from the input fields
  const level = document.getElementById("level").value;
  const school = document.getElementById("school").value;
  const dateStarted = document.getElementById("date-started").value;
  const dateCompleted = document.getElementById("date-completed").value;

  // Check if all fields are filled
  if (level && school && dateStarted && dateCompleted) {
    // Get the table body
    const tableBody = document.getElementById("education-list");

    // Create a new row
    const newRow = document.createElement("tr");

    // Create table cells for each piece of information
    newRow.innerHTML = `
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${level}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${school}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${dateStarted}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${dateCompleted}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
          <button class="text-red-600 hover:text-red-900" onclick="removeEducationalBackground(this)">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline-block" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8.707 9.293a1 1 0 011.414 0L12 11.586l1.879-1.879a1 1 0 111.414 1.414l-2.586 2.586a1 1 0 01-1.414 0L8.707 10.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </td>
      `;

    // Append the new row to the table
    tableBody.appendChild(newRow);

    // Reset the fields
    document.getElementById("level").value = "";
    document.getElementById("school").value = "";
    document.getElementById("date-started").value = "";
    document.getElementById("date-completed").value = "";
  } else {
    alert("Please fill in all fields before adding.");
  }
}

function removeEducationalBackground(button) {
  // Remove the row containing the clicked button
  button.closest("tr").remove();
}

function handleFiles(files) {
  const preview = document.getElementById("file-preview");
  preview.innerHTML = ""; // Clear existing previews

  Array.from(files).forEach((file) => {
    const fileItem = document.createElement("div");
    fileItem.classList.add(
      "flex",
      "items-center",
      "justify-between",
      "p-2",
      "border",
      "rounded-md",
      "mb-2"
    );

    const fileName = document.createElement("span");
    fileName.classList.add("text-sm", "text-gray-700");
    fileName.textContent = file.name;

    const removeButton = document.createElement("button");
    removeButton.classList.add(
      "text-red-500",
      "hover:text-red-700",
      "focus:outline-none"
    );
    removeButton.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>';

    removeButton.onclick = () => {
      const newFileList = Array.from(files).filter((f) => f !== file);
      handleFiles(newFileList);
    };

    fileItem.appendChild(fileName);
    fileItem.appendChild(removeButton);
    preview.appendChild(fileItem);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  flatpickr("#dob", {
    dateFormat: "Y-m-d",
  });
});
