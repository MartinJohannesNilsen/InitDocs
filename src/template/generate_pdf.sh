# Generate static site
docker compose up docs-build

# Generate pdf through docker container, placed inside /site
docker run -v "$(pwd)/site:/workspace" pink33n/html-to-pdf --url http://localhost/print_page.html --pdf documentation.pdf