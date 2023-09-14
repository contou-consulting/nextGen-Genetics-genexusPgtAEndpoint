docker build -t genexus-pgta-endpoint .
docker save -o genexus-pgta-endpoint.tar genexus-pgta-endpoint:latest
Copy-Item ".\genexus-pgta-endpoint.tar" "C:\Users\KyleVanderstoep\OneDrive - Contou Inc\Shared\NextGen\genexus-pgta-endpoint.tar"