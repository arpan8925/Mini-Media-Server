# Media Server Software

This repository contains all the necessary files and database needed to set up a fully functional Media Server website built with Python FastAPI.

![LMS Website Screenshot](Screenshot_88.png)

## Project Overview

The project is a Media Server built using Python, FastAPI, and Jinja2Templating. The software allows you to host media on your own computer and get a direct link to the media by clicking it.

## Project Structure

Below is an image representation of the project structure:

![Project Structure](Screenshot_87.png)

- **media_storage/**: Contains the media files that are hosted on the server.
  - **Foods/**: Directory for food-related media files.
  - **Inventory/**: Directory for inventory-related media files.
  
- **static/**: Contains static files like CSS and JavaScript.
  - **css/**: Contains styles for the website.
    - `styles.css`: Main stylesheet for the site.
  - **js/**: Contains JavaScript files.
    - `script.js`: JavaScript file for website functionality.

- **templates/**: Contains HTML templates for rendering web pages.
  - `base.html`: Base template for the site layout.
  - `index.html`: Homepage of the site.

- **main.py**: The main Python file that runs the FastAPI application.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you have improvements or suggestions, feel free to submit an issue or a pull request.

## Contact

If you have any questions or need help setting up the site, feel free to reach out:

- **Email**: [your-email@example.com](mailto:your-email@example.com)
- **GitHub**: [Your GitHub Profile](https://github.com/your-profile)

---

Thank you for using this Media Server software! Feel free to clone, fork, and contribute to improve the experience further.
