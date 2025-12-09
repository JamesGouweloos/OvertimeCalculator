# Deployment Guide for Overtime Analysis Platform

This guide covers multiple deployment options for hosting the Overtime Analysis Platform.

## Quick Deploy Options (Recommended)

### Option 1: Render (Easiest - Free Tier Available) ⭐ RECOMMENDED

**Pros:**
- Free tier available (with limitations)
- Very easy setup
- Automatic HTTPS
- Good for Flask apps
- Auto-deploy from GitHub

**Steps:**

1. **Prepare your code:**
   - Ensure all files are committed to a GitHub repository
   - The `render.yaml` file is already configured

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up/login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

3. **Configure (if needed):**
   - The app will be available at: `https://your-app-name.onrender.com`
   - Free tier: App sleeps after 15 minutes of inactivity
   - Upgrade to paid plan for always-on service

**Cost:** Free (with limitations) or $7/month for always-on

---

### Option 2: Railway (Very Easy - Free Trial)

**Pros:**
- $5 free credit monthly
- Very easy deployment
- Auto-detects Flask apps
- Good performance

**Steps:**

1. **Deploy on Railway:**
   - Go to https://railway.app
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect and deploy
   - The `railway.json` is already configured

2. **Access your app:**
   - Railway provides a URL automatically
   - Example: `https://your-app-name.up.railway.app`

**Cost:** $5/month after free trial credit

---

### Option 3: PythonAnywhere (Python-Focused)

**Pros:**
- Free tier available
- Python-focused platform
- Good for learning

**Steps:**

1. **Sign up:**
   - Go to https://www.pythonanywhere.com
   - Create a free account

2. **Upload files:**
   - Use the Files tab to upload all project files
   - Or use Git: `git clone https://github.com/your-repo.git`

3. **Configure Web App:**
   - Go to Web tab
   - Click "Add a new web app"
   - Choose Flask
   - Set source code directory
   - Set WSGI file to: `/home/yourusername/mysite/app.py`
   - Update WSGI file to point to your Flask app

4. **Install dependencies:**
   - Go to Bash console
   - Run: `pip3.10 install --user -r requirements.txt`

5. **Reload web app:**
   - Click "Reload" in Web tab

**Cost:** Free (limited) or $5/month for better performance

---

## Self-Hosted Options

### Option 4: VPS with Gunicorn + Nginx

**Best for:** Full control, production use

**Requirements:**
- VPS (DigitalOcean, Linode, AWS EC2, etc.)
- Domain name (optional)

**Steps:**

1. **Set up server:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3 python3-pip python3-venv nginx -y
   ```

2. **Deploy application:**
   ```bash
   # Clone repository
   git clone https://github.com/your-repo.git
   cd OvertimeCalculator
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Create systemd service:**
   Create `/etc/systemd/system/overtime-calc.service`:
   ```ini
   [Unit]
   Description=Overtime Calculator Gunicorn daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/OvertimeCalculator
   Environment="PATH=/path/to/OvertimeCalculator/venv/bin"
   ExecStart=/path/to/OvertimeCalculator/venv/bin/gunicorn \
             --workers 3 \
             --bind unix:/path/to/OvertimeCalculator/overtime-calc.sock \
             app:app

   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx:**
   Create `/etc/nginx/sites-available/overtime-calc`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/OvertimeCalculator/overtime-calc.sock;
       }

       location /static {
           alias /path/to/OvertimeCalculator/static;
       }
   }
   ```

5. **Enable and start:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/overtime-calc /etc/nginx/sites-enabled/
   sudo systemctl start overtime-calc
   sudo systemctl enable overtime-calc
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. **Set up SSL (Let's Encrypt):**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

**Cost:** $5-20/month depending on VPS provider

---

### Option 5: Docker Deployment

**Best for:** Containerized deployments, Kubernetes

**Create `Dockerfile`:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2"]
```

**Deploy:**
- Can be deployed to any Docker-compatible platform
- AWS ECS, Google Cloud Run, Azure Container Instances
- Or use Docker Compose for local deployment

---

## Environment Variables (if needed)

For production, you may want to set:
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`
- `PORT=5000` (usually set by platform)

---

## Recommendations

1. **For quick testing:** Use Render (free tier)
2. **For production:** Use Railway or VPS with Nginx
3. **For learning:** Use PythonAnywhere
4. **For enterprise:** Use AWS/GCP/Azure with proper infrastructure

---

## Post-Deployment Checklist

- [ ] Test file upload functionality
- [ ] Verify all API endpoints work
- [ ] Check that static files load correctly
- [ ] Test with sample Excel files
- [ ] Set up monitoring (optional)
- [ ] Configure backups (if using VPS)
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS/SSL

---

## Troubleshooting

**Issue: App crashes on file upload**
- Increase timeout in gunicorn command
- Check file size limits
- Verify uploads directory permissions

**Issue: Static files not loading**
- Check static file paths
- Verify Nginx configuration (if using)
- Check Flask static folder configuration

**Issue: Memory errors**
- Reduce gunicorn workers
- Increase server memory
- Optimize pandas operations

---

## Support

For deployment issues, check:
- Platform-specific documentation
- Flask deployment guide: https://flask.palletsprojects.com/en/latest/deploying/
- Gunicorn documentation: https://docs.gunicorn.org/

