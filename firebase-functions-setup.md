# Firebase Functions Setup (Alternative Approach)

If Firebase App Hosting is not available, you can use Firebase Functions + Hosting.

## Setup Steps

1. **Install Firebase CLI**:
```bash
npm install -g firebase-tools
firebase login
```

2. **Initialize Firebase**:
```bash
firebase init functions
# Select Python when prompted
# Choose your Firebase project
```

3. **Update `functions/main.py`**:
```python
from flask import Flask
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app

# Export for Firebase Functions
app = flask_app
```

4. **Update `functions/requirements.txt`**:
Copy your requirements.txt content to `functions/requirements.txt`

5. **Deploy**:
```bash
firebase deploy --only functions,hosting
```

## Note

Firebase Functions has limitations:
- 60-second timeout (can be extended to 540 seconds)
- File size limits
- Cold start times

For better performance, consider Cloud Run deployment instead.

