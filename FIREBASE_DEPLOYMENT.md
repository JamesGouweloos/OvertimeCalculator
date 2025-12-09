# Firebase App Hosting Deployment Guide

This guide will help you deploy the Overtime Analysis Platform to Firebase App Hosting.

## Prerequisites

1. **Firebase Account**: Sign up at https://firebase.google.com
2. **Firebase CLI**: Install Firebase CLI tools
3. **Node.js**: Required for Firebase CLI (even though we're deploying Python)
4. **Git**: Your code should be in a Git repository (GitHub recommended)

## Step 1: Install Firebase CLI

```bash
# Install Firebase CLI globally
npm install -g firebase-tools

# Login to Firebase
firebase login
```

## Step 2: Initialize Firebase Project

```bash
# Navigate to your project directory
cd OvertimeCalculator

# Initialize Firebase (if not already done)
firebase init

# Select:
# - App Hosting (if available)
# - Or Functions + Hosting
# - Choose your Firebase project or create a new one
```

## Step 3: Configure Firebase Project

1. **Update `.firebaserc`**:
   - Replace `your-project-id` with your actual Firebase project ID
   - Or run `firebase use --add` to add your project

2. **Verify `apphosting.yaml`**:
   - The configuration file is already created
   - It specifies Python 3.12 runtime
   - Configures Gunicorn for production

## Step 4: Deploy to Firebase App Hosting

### Option A: Using Firebase CLI (Recommended)

```bash
# Deploy to App Hosting
firebase deploy --only hosting

# Or if using App Hosting specifically:
firebase apphosting:backends:create
```

### Option B: Using Firebase Console

1. Go to Firebase Console: https://console.firebase.google.com
2. Select your project
3. Navigate to "App Hosting" (if available)
4. Click "Create backend"
5. Connect your GitHub repository
6. Firebase will auto-detect the `apphosting.yaml` configuration
7. Click "Deploy"

## Step 5: Alternative - Firebase Functions + Hosting

If App Hosting is not available in your region, use Functions + Hosting:

### Deploy Functions:

```bash
# Deploy the backend function
firebase deploy --only functions
```

### Deploy Hosting:

```bash
# Build static files (if needed)
# Deploy hosting
firebase deploy --only hosting
```

## Step 6: Update Firebase Configuration

If using Functions + Hosting approach, update `firebase.json`:

```json
{
  "hosting": {
    "public": "static",
    "rewrites": [
      {
        "source": "/api/**",
        "function": "app"
      },
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  },
  "functions": {
    "source": ".",
    "runtime": "python312"
  }
}
```

## Step 7: Environment Variables (if needed)

Set environment variables in Firebase Console:

1. Go to Firebase Console → Functions → Configuration
2. Add environment variables:
   - `FLASK_ENV=production`
   - `FLASK_DEBUG=False`

Or use Firebase CLI:

```bash
firebase functions:config:set flask.env="production"
```

## Troubleshooting

### Issue: App Hosting not available
- **Solution**: Use Firebase Functions + Hosting instead
- Or use Cloud Run (see alternative deployment)

### Issue: Python runtime not found
- **Solution**: Ensure `runtime: python312` in `apphosting.yaml`
- Check Firebase documentation for supported Python versions

### Issue: Static files not loading
- **Solution**: Verify `firebase.json` rewrites configuration
- Check that static files are in the correct directory

### Issue: File uploads not working
- **Solution**: Firebase Functions have file size limits
- Consider using Firebase Storage for file uploads
- Or increase function timeout in `firebase.json`

## Alternative: Cloud Run Deployment

If App Hosting doesn't work, deploy to Cloud Run:

1. **Create `Dockerfile`**:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2"]
```

2. **Deploy to Cloud Run**:
```bash
# Build and deploy
gcloud run deploy overtime-calculator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Post-Deployment

1. **Test the deployment**:
   - Visit your Firebase hosting URL
   - Test file upload functionality
   - Verify all API endpoints work

2. **Set up custom domain** (optional):
   - Firebase Console → Hosting → Add custom domain
   - Follow DNS configuration instructions

3. **Enable HTTPS**:
   - Firebase automatically provides SSL certificates
   - No additional configuration needed

## Cost Considerations

- **Firebase Hosting**: Free tier includes 10GB storage, 360MB/day transfer
- **Firebase Functions**: Free tier includes 2 million invocations/month
- **Cloud Run**: Free tier includes 2 million requests/month
- **App Hosting**: Check current pricing on Firebase website

## Support Resources

- Firebase Documentation: https://firebase.google.com/docs
- App Hosting Docs: https://firebase.google.com/docs/app-hosting
- Firebase Support: https://firebase.google.com/support

## Notes

- Firebase App Hosting is still in preview/beta in some regions
- If unavailable, use Firebase Functions + Hosting as alternative
- For production workloads, consider Cloud Run for better scalability
- File uploads may need Firebase Storage integration for large files

