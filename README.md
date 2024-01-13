# Description

The goal of this project is to package and distribute an application using Docker containers. The selected application
to containerize will be capable of displaying a graph containing information about restaurants and chefs in a web interface.
To build this application, three containers will be necessary.

1. Preprocessing and Graph Construction Container:

- Responsible for preprocessing data to construct the graph.
- Creates and manages the graph.
- Connects to a MongoDB database to ensure data persistence.

2. MongoDB Container:

- Hosts the MongoDB database.
- Connected to by the preprocessing and graph construction container for data storage.

3. Web Server Container (Flask):

- Hosts the web server.
- Built using Flask.
- Interfaces with the constructed graph and MongoDB for data retrieval and display.

This containerized architecture allows for better modularity, scalability, and ease of deployment. Each container has a
specific role, and Docker facilitates the encapsulation of dependencies, ensuring consistent behavior across different
environments. The use of MongoDB enhances data persistence, and Flask simplifies the development of the web server.
This approach makes it easier to manage, deploy, and scale the application in various environments.

# Execution

To create the container hosting the MongoDB database, an official MongoDB image available on DockerHub was directly used.
The tag used was 3.0.2. However, the containers for graph-processing and graph-web need to be created first.

To achieve this, individual Dockerfiles have been created. The content of both is quite similar.
In the case of graph-processing, it started with a Python 3.6 image. Subsequently, the requirements_graph.txt file was
copied, specifying the necessary Python libraries that are installed using the "pip install" command.
Additionally, the necessary files were copied from the host (in this case, the preprocessing script) to
finally launch the script using the "python process_graph.py" command. Similarly, the Dockerfile associated with the web server has been created.

These images are built using the docker-compose.dev.yml file. Later, both images have been published on DockerHub,
so they can be subsequently downloaded directly from there.

To run the service:

```
docker-compose up
```