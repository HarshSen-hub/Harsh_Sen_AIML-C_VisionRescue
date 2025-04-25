const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const usersFile = path.join(__dirname, 'data', 'users.json');
const reportsFile = path.join(__dirname, 'data', 'reports.json');

function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

function handleRequest(req, res) {
  if (req.method === 'GET' && req.url === '/') {
    return sendJSON(res, 200, { message: 'Vision Rescue Backend Running' });
  }

  if (req.method === 'POST') {
    let body = '';

    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      const parsed = JSON.parse(body || '{}');

      if (req.url === '/signup') {
        const users = JSON.parse(fs.readFileSync(usersFile, 'utf8'));
        users.push({ email: parsed.email, password: parsed.password });
        fs.writeFileSync(usersFile, JSON.stringify(users, null, 2));
        return sendJSON(res, 201, { message: 'User signed up successfully' });
      }

      if (req.url === '/login') {
        const users = JSON.parse(fs.readFileSync(usersFile, 'utf8'));
        const user = users.find(u => u.email === parsed.email && u.password === parsed.password);
        if (user) {
          return sendJSON(res, 200, { message: 'Login successful' });
        } else {
          return sendJSON(res, 401, { message: 'Invalid credentials' });
        }
      }

      if (req.url === '/report') {
        const reports = JSON.parse(fs.readFileSync(reportsFile, 'utf8'));
        reports.push(parsed);
        fs.writeFileSync(reportsFile, JSON.stringify(reports, null, 2));
        return sendJSON(res, 201, { message: 'Report submitted' });
      }

      if (req.url === '/search') {
        const reports = JSON.parse(fs.readFileSync(reportsFile, 'utf8'));
        const results = reports.filter(r => r.name.toLowerCase().includes(parsed.name.toLowerCase()));
        return sendJSON(res, 200, { results });
      }

      sendJSON(res, 404, { message: 'Route not found' });
    });
  } else {
    sendJSON(res, 405, { message: 'Method Not Allowed' });
  }
}

http.createServer(handleRequest).listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
