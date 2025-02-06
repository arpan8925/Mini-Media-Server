window.onload = function () {
    // Initialize window.imageData with all images when the page loads
    window.imageData = Array.from(document.querySelectorAll(".column img")).map(img => ({
        src: img.src,
        alt: img.alt
    }));
};

function loadImages(category) {
    fetch(`/get_images/${category}`)
        .then(response => response.json())
        .then(data => {
            let container = document.querySelector('.row'); 
            container.innerHTML = "";  // Clear previous images

            if (data.error) {
                container.innerHTML = `<p>${data.error}</p>`;
                return;
            }

            // Update window.imageData with the current category's images
            window.imageData = data.images;

            // Render images in grid view
            data.images.forEach(img => {
                let column = document.createElement('div');
                column.classList.add('column');
                column.onclick = function () { copyURL(this); };

                let overlayDiv = document.createElement('div');
                overlayDiv.classList.add('shine-overlay');

                let imageElement = document.createElement('img');
                imageElement.src = img.src;
                imageElement.alt = img.alt;

                let shineDiv = document.createElement('div');
                shineDiv.classList.add('shine');

                let tooltip = document.createElement('span');
                tooltip.classList.add('tooltip');
                tooltip.textContent = "Click to Copy URL";

                overlayDiv.appendChild(imageElement);
                overlayDiv.appendChild(shineDiv);
                column.appendChild(overlayDiv);
                column.appendChild(tooltip);
                container.appendChild(column);
            });
        });
}

function showAllImages() {
    let container = document.querySelector('.row'); 
    container.innerHTML = "";  // Clear previous images

    // Update window.imageData with all images
    window.imageData = allImages; // Use the globally defined allImages

    // Render images in grid view
    allImages.forEach(img => {
        let column = document.createElement('div');
        column.classList.add('column');
        column.onclick = function () { copyURL(this); }; // Pass 'this' instead of img.src

        let overlayDiv = document.createElement('div');
        overlayDiv.classList.add('shine-overlay');

        let imageElement = document.createElement('img');
        imageElement.src = img.src;
        imageElement.alt = img.alt;

        let shineDiv = document.createElement('div');
        shineDiv.classList.add('shine');

        let tooltip = document.createElement('span');
        tooltip.classList.add('tooltip');
        tooltip.textContent = "Click to Copy URL";

        overlayDiv.appendChild(imageElement);
        overlayDiv.appendChild(shineDiv);
        column.appendChild(overlayDiv);
        column.appendChild(tooltip);
        container.appendChild(column);
    });
}

function copyURL(element) {
    let imgSrc = element.querySelector("img").src; // Get the image source
    let tooltip = element.querySelector(".tooltip");

    // Copy URL to clipboard
    navigator.clipboard.writeText(imgSrc).then(() => {
        tooltip.innerText = "Copied!";
        tooltip.style.visibility = "visible"; // Show tooltip
        tooltip.style.opacity = "1"; // Make it fully visible

        // Hide tooltip after 1.5 seconds
        setTimeout(() => {
            tooltip.innerText = "Click to copy";
            tooltip.style.visibility = "hidden"; // Hide tooltip
            tooltip.style.opacity = "0"; // Fade out
        }, 1500);
    }).catch(err => console.error("Failed to copy: ", err));
}


function gridView() {
    const container = document.querySelector(".row");
    container.innerHTML = ""; // Clear existing content

    // Render images from window.imageData in grid view
    window.imageData.forEach(img => {
        const column = document.createElement('div');
        column.className = 'column';
        column.onclick = () => copyURL(column);

        const overlayDiv = document.createElement('div');
        overlayDiv.className = 'shine-overlay';

        const imageElement = new Image();
        imageElement.src = img.src;
        imageElement.alt = img.alt;

        const shineDiv = document.createElement('div');
        shineDiv.className = 'shine';

        const tooltip = document.createElement('span');
        tooltip.className = 'tooltip';
        tooltip.textContent = "Click to Copy URL";

        overlayDiv.appendChild(imageElement);
        overlayDiv.appendChild(shineDiv);
        column.appendChild(overlayDiv);
        column.appendChild(tooltip);
        container.appendChild(column);
    });

    // Apply grid-specific styles
    container.style.display = 'flex';
    container.style.flexWrap = 'wrap';
    container.querySelectorAll('.column').forEach(column => {
        column.style.width = '10%'; // Adjust based on your grid requirements
    });
}





function listView() {
    const container = document.querySelector(".row");

    // Ensure full-width parent container
    container.style.display = "block";
    container.style.width = "100%";

    // Create Table Structure
    let tableHTML = `
        <div style="width: 100%;">
            <table id="mediaTable" class="display nowrap" style="width:100%">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Name</th>
                    </tr>
                </thead>
                <tbody>
    `;

    // Use the updated window.imageData array
    window.imageData.forEach(data => {
        tableHTML += `
            <tr onclick="copyURL(this)">
                <td><img src="${data.src}" width="50" height="50" style="border-radius: 5px;"></td>
                <td>${data.alt}</td>
                <span class="tooltip">Test</span>
            </tr>
        `;
    });

    tableHTML += `
                </tbody>
            </table>
        </div>
    `;

    // Replace Grid with Table
    container.innerHTML = tableHTML;

    // Apply DataTables
    $(document).ready(function () {
        $('#mediaTable').DataTable({
            paging: true,
            searching: true,
            ordering: true,
            autoWidth: false,
            responsive: true,
            lengthChange: false
        });

        // Ensure DataTable Wrapper takes full width
        $("#mediaTable_wrapper").css({
            "width": "100%",
            "max-width": "100%",
            "margin": "0 auto"
        });

        // Fix Parent Container
        $(".main-content").css({
            "width": "100%",
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center"
        });
    });
}


document.addEventListener("DOMContentLoaded", function () {
    var btns = document.querySelectorAll(".btn"); // Select all buttons

    btns.forEach(function (btn) {
        btn.addEventListener("click", function () {
            // Remove active class from all buttons
            btns.forEach(function (b) {
                b.classList.remove("active");
            });

            // Add active class to the clicked button
            this.classList.add("active");
        });
    });
});


