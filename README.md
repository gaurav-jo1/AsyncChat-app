# AsyncChat-App

Welcome to **AsyncChat**, AsyncChat-App is a portfolio project designed to demonstrate the capabilities of real-time chat protocols, making it ideal for live communication scenarios.

## Technologies Used:

**Backend:** 🌐 Built with Python and Django, AsyncChat-App ensures secure and scalable server-side operations. Integration of Redis enhances performance, while PostgreSQL handles data storage efficiently.

**Frontend:** 🎨 Utilizing TypeScript and React, AsyncChat-App offers a dynamic and responsive user interface. SCSS is employed for streamlined styling, ensuring a visually appealing and intuitive user experience.

**Infrastructure:** 🐳 Docker and GitHub Actions are instrumental in automating deployment and continuous integration processes, maintaining project reliability and consistency. AsyncChat-App's architecture is adaptable, suitable for scaling and building infrastructures similar to advanced systems like ChatGPT.

**Testing:** 🧪 Pytest is implemented for rigorous backend testing, ensuring code quality and reliability throughout development cycles.

## Getting Started 🔥

To get started with the project, follow these steps:

1. **Clone the repository to your local machine:**
   ```sh
   git clone https://github.com/gaurav-jo1/AsyncChat-app
   ```

3. **Navigate to the project directory:**
   ```sh
   cd AsyncChat-app
   ```

4. **Install frontend dependencies:**
   ```sh
   cd frontend && npm install
   ```

5. **Set up the backend environment (optional for development):**
   - Create a virtual environment:
     ```sh
     cd backend && virtualenv venv
     ```
   - Activate the virtual environment and install dependencies:
     ```sh
     source ./venv/bin/activate && pip install -r requirements.txt
     ```

6. **Set up the database configuration:**
   - Navigate to the database directory and create the `postgres_auth.txt` file:
     ```sh
     cd database/ && echo "postgres" > postgres_auth.txt
     ```

7. **Run the application:**
   - Navigate to the root directory and start the services with Docker:
     ```sh
     docker compose up
     ```

Access the application at: 🔗 http://localhost:5173

That's it! You should now be able to get started with the project and use Docker Compose to run the application. If you have any questions or issues, feel free to open an issue on the repository. Thanks for using my project!

