# Odoo OpenELIS Connector

This project provides integration between Odoo and OpenELIS systems using a clean Maven-based approach for managing dependencies and configurations.

## Overview

The project uses Maven to manage the Odoo initializer addon dependency, providing a cleaner and more maintainable approach compared to manually copying files.

## Architecture

The project follows a modular architecture with the following components:

- **Odoo Initializer Addon**: Automatically managed via Maven dependency
- **OpenELIS Configuration**: Local configuration files for OpenELIS setup
- **Docker Compose**: Containerized deployment setup
- **Nginx Configuration**: Reverse proxy configuration

## Build Process

### Prerequisites

- Java 8 or higher
- Maven 3.6 or higher
- Docker and Docker Compose

### Building the Distribution

The project uses Maven to build a distributable package:

```bash
mvn clean package
```

This will:
1. Download the Odoo initializer addon from the Mekom Solutions repository (if available)
2. Fall back to local files if the remote dependency is not accessible
3. Package all configurations into a distributable archive

### Build Artifacts

After a successful build, you'll find the following artifacts in the `target/` directory:

- `odoo-openelis-connector-1.0.0-SNAPSHOT.tar.gz` - Compressed distribution package
- `odoo-openelis-connector-1.0.0-SNAPSHOT.zip` - ZIP distribution package

## Dependency Management

### Odoo Initializer Addon

The Odoo initializer addon is managed as a Maven dependency:

```xml
<dependency>
    <groupId>net.mekomsolutions.odoo</groupId>
    <artifactId>odoo-initializer</artifactId>
    <version>2.3.0-SNAPSHOT</version>
    <type>zip</type>
    <optional>true</optional>
</dependency>
```

**Key Features:**
- **Automatic Download**: Maven attempts to download the latest version from the Mekom Solutions repository
- **Fallback Mechanism**: If the remote dependency is unavailable, the build falls back to local files
- **Version Management**: Easy version updates by changing the version property in `pom.xml`

### Repository Configuration

The project is configured to use the Mekom Solutions Maven repository:

```xml
<repository>
    <id>mekom-solutions</id>
    <name>Mekom Solutions Repository</name>
    <url>https://maven.mekomsolutions.com/repository/public/</url>
</repository>
```

## Project Structure

```
odoo-openelis-connector/
├── configs/
│   ├── nginx/           # Nginx configuration
│   ├── odoo/            # Odoo configuration and addons
│   │   ├── addons/      # Odoo addons (managed by Maven)
│   │   └── config/      # Odoo configuration files
│   └── openelis/        # OpenELIS configuration
├── docker-compose.yml   # Docker Compose configuration
├── pom.xml             # Maven project configuration
├── assembly.xml        # Maven assembly descriptor
└── README.md           # This file
```

## Deployment

### Quick Start (Recommended)

Use the provided deployment scripts for easy setup:

#### For Development:
```bash
./setup-dev.sh
```

#### For Production:
```bash
./deploy.sh
```

### Manual Deployment

#### Option 1: Using the Built Distribution Package

1. Build the distribution:
   ```bash
   mvn clean package
   ```

2. Extract the distribution package:
   ```bash
   cd target
   tar -xzf odoo-openelis-connector-1.0.0-SNAPSHOT.tar.gz
   cd odoo-openelis-connector-1.0.0-SNAPSHOT
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

#### Option 2: Development Mode

1. Prepare the development environment:
   ```bash
   ./setup-dev.sh
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

### Service Access

Once deployed, the services will be available at:

- **Odoo**: http://localhost:8069
- **OpenELIS**: https://localhost:8443
- **FHIR API**: http://localhost:8081

### Useful Docker Compose Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View service status
docker-compose ps
```

## Configuration

### Odoo Configuration

The Odoo configuration is located in `configs/odoo/` and includes:
- Addon configurations
- Database initialization scripts
- Custom module configurations

### OpenELIS Configuration

OpenELIS configuration files are in `configs/openelis/` and include:
- Database configuration
- Application properties
- Logging configuration

## Development

### Adding New Dependencies

To add new Maven dependencies:

1. Add the dependency to the `dependencies` section in `pom.xml`
2. Configure the appropriate Maven plugin to handle the dependency
3. Update the assembly descriptor if needed

### Updating Odoo Initializer Version

To update the Odoo initializer version:

1. Update the `odooInitializerVersion` property in `pom.xml`
2. Run `mvn clean package` to rebuild with the new version

### CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline with the following workflows:

- **Main CI/CD Pipeline**: Core testing and building
- **Quality Checks**: Code quality and security scanning
- **Release Pipeline**: Automated GitHub releases

For detailed information, see [CI.md](CI.md).

#### Local Quality Checks

```bash
# Validate Maven project
mvn validate

# Analyze dependencies
mvn dependency:analyze

# Security vulnerability scan
mvn org.owasp:dependency-check-maven:check

# Build distribution
mvn clean package
```

## Troubleshooting

### Network Issues with Remote Repository

If you encounter network issues with the Mekom Solutions repository:

1. The build will automatically fall back to local files
2. Ensure the local `configs/odoo/addons/odoo_initializer/` directory contains the required files
3. Check your network connectivity to `maven.mekomsolutions.com`

### Build Failures

If the build fails:

1. Check that all required dependencies are available
2. Verify the Maven configuration in `pom.xml`
3. Ensure the local fallback files are present

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the build process
5. Submit a pull request

## License

This project is licensed under the terms specified in the project documentation.
