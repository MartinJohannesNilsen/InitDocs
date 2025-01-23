# Generate static site
docker compose run --rm docs-build

# Generate pdf through docker container, placed inside /site
docker run --rm -v "$(pwd)/site:/workspace" pink33n/html-to-pdf --url http://localhost/print_page.html --pdf documentation.pdf