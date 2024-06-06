const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = process.env.PORT || 3000; // Use the port specified in the environment variable or default to 3000

const server = http.createServer((req, res) => {
    let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
    let contentType = 'text/html';

    // Check the file extension to set the content type
    const extname = path.extname(filePath);
    switch (extname) {
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.css':
            contentType = 'text/css';
            break;
        case '.json':
            contentType = 'application/json';
            break;
        case '.png':
            contentType = 'image/png';
            break;
        case '.jpg':
            contentType = 'image/jpg';
            break;
    }

    // Read the file
    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                // Page not found
                res.writeHead(404);
                res.end('404 - Not Found');
            } else {
                // Server error
                res.writeHead(500);
                res.end(`Server Error: ${err.code}`);
            }
        } else {
            // Success
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

function getIPAddress() {
    const ifaces = os.networkInterfaces();
    for (const ifaceName of Object.keys(ifaces)) {
        // Check if the interface name contains 'Wi-Fi' (assuming Windows)
        if (ifaceName.toLowerCase().includes('wi-fi')) {
            const iface = ifaces[ifaceName];
            for (const details of iface) {
                if (details.family === 'IPv4' && !details.internal) {
                    return details.address;
                }
            }
        }
    }
    return null; // Return null if no IPv4 address is found
}

console.log(`Server will be hosted on: ${getIPAddress()}`);

server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
