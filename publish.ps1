docker build --build-arg FLASK_APP_USERNAME=7v478oudKFuLNbd5pW49 --build-arg FLASK_APP_PASSWORD=Z4e7oXH3A3VPNyG3pN1c --build-arg FLASK_ENV=development -t genexus-pgta-endpoint .
docker save -o genexus-pgta-endpoint.tar genexus-pgta-endpoint:latest
Copy-Item ".\genexus-pgta-endpoint.tar" "C:\Users\KyleVanderstoep\OneDrive - Contou Inc\Shared\NextGen\genexus-pgta-endpoint.tar"